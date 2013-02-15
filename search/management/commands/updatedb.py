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
                # Sometimes the data has an extra column.  Ignore it.
                if row.has_key(None):
                    row.pop(None)
                self.validate_and_add(row, line)


    def split_row(self, row, name, depth, line):
        r = DELIMITER.split(row)
        if len(r) != 1:
            if (depth != 1 and len(r) != depth):
                raise DBImportError(
                    "Error on line %d: Number of row sub-values does not match in"
                    "each column. %s has %d values, while previous columns had %d"
                    "values." % (line, name, len(r), depth))
            depth = len(r)
        return r, depth


    def validate_and_add(self, row, line):
        """
        Perform basic validation of the data in the row.
        """
        # The number of delimited values in the row. Supposedly, for each column
        # this will be n where n == 1 or n is the same for all columns in row
        depth = 1
        row_singles = {}
        row_multis = []
        #NOTE only trans. fac, expt, cell line/organ can have multi-value

        if not len(row['gene']) <= 255:
            raise DBImportError("Genes must be <= 255 characters. Got: '%s'"
                                % row['gene'])
    
        # Make sure pmid can be made an int, but pass on empty strings.
        if row['pmid'] != '':
            try:
                int(row['pmid'])
            except ValueError:
                raise DBImportError("PMIDs must be valid integers. Got '%s'" %
                                    row['pmid'])
        else:
            row['pmid'] = None
    
        # Split up the row, and check that the depth is valid
        expts, depth = self.split_row(row['expt_type'], 'Experiment type', depth, line)
        # If our list of multis is too short, grow it
        while len(row_multis) < depth:
            row_multis.append({})
        # Then, put each item in the row into the appropriate place
        for n, expt in enumerate(expts):
            if len(expts) == 1:
                row_singles['expt_type'] = expt
            else:
                row_multis[n]['expt_type'] = expt
        
        cell_lines, depth = self.split_row(row['cell_line'], 'Cell line', depth, line)
        while len(row_multis) < depth:
            row_multis.append({})
        for n, cell_line in enumerate(cell_lines):
            if len(cell_lines) == 1:
                row_singles['cell_line'] = cell_line
            else:
                row_multis[n]['cell_line'] = cell_line
        
        transcription_factors, depth = self.split_row(row['transcription_factor'], 'Transcription factor', depth, line)
        while len(row_multis) < depth:
            row_multis.append({})
        for n, transcription_factor in enumerate(transcription_factors):
            if len(transcription_factors) == 1:
                row_singles['transcription_factor'] = transcription_factor
            else:
                row_multis[n]['transcription_factor'] = transcription_factor

        # Now we can finally add rows
        for values in row_multis:
            values.update(row_singles)
            e = Experiment(**values)
            e.save()

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
