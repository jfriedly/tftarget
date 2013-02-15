from django.core.management.base import BaseCommand, CommandError
import csv
import re

from search.models import Experiment

# We use this a lot, so we should only compile it once.
DELIMITER = re.compile('\s*[/;,+&]+\s*')

class DBImportError(Exception):
    message = ''

    def __init__(self, message=None):
        if message:
            self.message = message
        super(DBImportError, self).__init__(self.message)


class Command(BaseCommand):
    args = 'filename'
    help = ("Updates the database with new rows from a CSV file.\n\n"
            "The CSV file should use tab characters to separate values.\n"
            "You can create a CSV in Excel by using 'Save as...' and\n"
            "selecting .csv or by using 'Export'.\n")

    def handle(self, *args, **options):
        # This is the expected order of columns. It can easily be re-arranged.
        columns = ['gene', 'transcription_factor', 'pmid', 'species',
                   'expt_tissues', 'cell_line', 'expt_type', 'replicates',
                   'control', 'quality']
        if len(args) != 1:
            raise CommandError("Please give one and only one filename.")

        #(jfriedly) I considered putting this in a try: except IOError, but I
        # think it's better to just let that bubble up.
        with open(args[0], 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=columns,
                                    delimiter='\t')
            # Skip the first row (column names)
            r = reader.next()
            for line, row in enumerate(reader, start=1):
                row = self._validate_row(row, line)
                # Sometimes the data has an extra column.  Ignore it.
                if row.has_key(None):
                    row.pop(None)
                e = Experiment(**row)
                e.save()


    def _validate_row(self, row, line):
        """
        Perform basic validation of the data in the row.
        """
        # The number of delimited values in the row. Supposedly, for each column
        # this will be n where n == 1 or n is the same for all columns in row
        row_depth = 1

        # Check for valid gene
        if not len(row['gene']) <= 255:
            raise DBImportError("Genes must be <= 255 characters. Got: '%s'" %
                                row['gene'])

        # Make sure pmid can be made an int, but pass on empty strings.
        if row['pmid'] != '':
            try:
                int(row['pmid'])
            except ValueError:
                raise DBImportError("PMIDs must be valid integers. Got '%s'" %
                                    row['pmid'])
        else:
            row['pmid'] = None

        # Check Experiment types
        expt_types = DELIMITER.split(row['expt_type'])
        if len(expt_types) != 1 and (row_depth != 1 and len(expt_types) != row_depth):
            raise DBImportError(
                "Number of row sub-values does not match in each column."
                "Experiment type has %d values, while previous columns had %d"
                "values." % (len(expt_types), row_depth))
        self.check_experiment_types(expt_types)
        row['expt_type'] = ', '.join(expt_types)
        
        
        return row

    def check_experiment_types(self, expt_types):
        """
        Takes a list of experiment types and ensures that they are valid and
        extant.
        """
        # Matches one or more slash, semicolon, comma, plus sign, ampersand,
        # possibly with whitespace on either side.
        for expt_type in expt_types:
            expt_type = expt_type.strip().lower()
            # Sometimes they forget the dash in experiment names
            #expt_type = re.sub('qPCR', 'q-PCR', expt_type, flags=re.I)
            #expt_type = re.sub('Run on', 'run-on', expt_type, flags=re.I)
            #expt_type = re.sub('run off', 'run-off', expt_type, flags=re.I)
            # Found this typo in the data.  We can fix it for them.
            #expt_type = re.sub('Westernn', 'Western', expt_type, flags=re.I)

    def _custom_transcription_factor_regexes(self, experiment, tf):
        # This one isn't supposed to have a dash
        tf = re.sub('NF-kB', 'NFkB', tf, flags=re.I)
        # The data they give us may have Myc transcription factors as just
        # the letter for the family member.  We fix that here.
        if (experiment.transcription_family == Experiment.MYC and
            Experiment.MYC.lower() not in tf.lower()):
            tf = re.sub('(.*)', r'\1-Myc', tf, flags=re.I)
        # The data they give us may have STAT transcription factors as just
        # the digit for the family member.  We fix that here.
        if (experiment.transcription_family == Experiment.STAT and
            Experiment.STAT.lower() not in tf.lower()):
            tf = re.sub('(.*)', r'STAT\1', tf, flags=re.I)
        return tf
