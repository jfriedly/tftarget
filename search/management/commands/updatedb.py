from django.core.management.base import BaseCommand, CommandError
import csv
import re
import sys

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
            sys.stdout.write(args[0] + ' line:       ')
            errors = 0
            adds = 0
            dupes = 0
            for line, row in enumerate(reader, start=2):
                sys.stdout.write('\b'*5 + str(line).rjust(5))
                sys.stdout.flush()
                # Sometimes the data has an extra column.  Ignore it.
                if row.has_key(None):
                    row.pop(None)
                try:
                   added, dupe = self.validate_and_add(row, line)
                   adds += added
                   dupes += dupe
                except DBImportError as e:
                    #TODO make a file of these errors.
                    errors += 1
                    sys.stdout.write('\n%s\n%s line:      ' % (e, args[0]))
            print ('\nAdded %d/%d entries. Ignored %d errors and %d duplicates.'
                    % (adds, adds+dupes+errors, errors, dupes))

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
        row_multis = []
        #NOTE only trans. fac, expt, cell line/organ can have multi-value

        if not len(row['gene']) <= 255:
            raise DBImportError("Genes must be <= 255 characters. Got: '%s'"
                                % row['gene'])
    
        # Make sure pmid can be made an int, but pass on empty strings.
        if row['pmid'] and row['pmid'].lower() not in ['na', 'n/a']:
            try:
                int(row['pmid'])
            except ValueError:
                raise DBImportError("Error on line %d: PMID must be a valid"
                                    "integer. Got '%s'" % (line, row['pmid']))
        else:
            row['pmid'] = None
        
        if not row['expt_type']:
            raise DBImportError("Error on line %d: No experiment type." % line)
        # Split up the row, and check that the depth is valid
        expts, depth = self.split_row(row['expt_type'], 'Experiment type', depth, line)
        # If our list of multis is too short, grow it
        while len(row_multis) < depth:
            row_multis.append({})
        # Then, if there's more than one value, put them in the multi-value list
        if len(expts) != 1:
            row.pop('expt_type')
            for n, expt in enumerate(expts):
                row_multis[n]['expt_type'] = expt
        
        cell_lines, depth = self.split_row(row['cell_line'], 'Cell line', depth, line)
        while len(row_multis) < depth:
            row_multis.append({})
        if len(cell_lines) == 1:
            row.pop('cell_line')
            for n, cell_line in enumerate(cell_lines):
                row_multis[n]['cell_line'] = cell_line
        
        if not row['transcription_factor']:
            raise DBImportError("Error on line %d: No transcription factor." % line)
        transcription_factors, depth = self.split_row(row['transcription_factor'], 'Transcription factor', depth, line)
        while len(row_multis) < depth:
            row_multis.append({})
        if len(transcription_factors) != 1:
            row.pop('transcription_factor')
            for n, transcription_factor in enumerate(transcription_factors):
                row_multis[n]['transcription_factor'] = transcription_factor

        # Now we can finally add rows
        added = 0
        duplicates = 0
        for values in row_multis:
            values.update(row)
            e, created = Experiment.objects.get_or_create(**values)
            if not created:
                duplicates += 1
            else:
                added += 1
        return added, duplicates

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
