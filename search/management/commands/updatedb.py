from django.core.management.base import BaseCommand, CommandError
import csv
import re

from search.models import Experiment, ExperimentType, TranscriptionFactor


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
                   'experimental_tissues', 'cell_line',
                   'expt_type', 'replicates', 'control', 'quality']
        if len(args) != 1:
            raise CommandError("Please give one and only one filename.")

        transcription_family = args[0].split('.')[0]
        families = {f[0].lower(): f[0] for f in Experiment.TF_FAMILIES}
        if not transcription_family.lower() in families:
            print ("Please make the name of your file the same as the"
                   "transcription family of the factors in it. This will "
                   "likely be the name of the worksheet you are exporting "
                   "from.")
            return

        #(jfriedly) I considered putting this in a try: except IOError, but I
        # think it's better to just let that bubble up.
        with open(args[0], 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=columns,
                                    delimiter='\t')
            # Skip the first row (column names)
            r = reader.next()
            for row in reader:
                row = self._validate_row(row)
                row['transcription_family'] = families[transcription_family]
                expt_types = row.pop('expt_type')
                tf_names = row.pop('transcription_factor')
                # Sometimes the data has an extra column.  Ignore it.
                if row.has_key(None):
                    row.pop(None)
                e = Experiment(**row)
                e.save()
                self.add_experiment_types(e, expt_types)
                self.add_transcription_factors(e, tf_names)

    def add_experiment_types(self, experiment, expt_types):
        """
        Takes string of experiment types, splits them, and ensures that they
        are valid and extant. Asks user to confirm addition of new type if not.
        """
        # Matches one or more slash, semicolon, comma, plus sign, ampersand,
        # possibly with whitespace on either side.
        delimiter = re.compile('\s*[/;,+&]+\s*')
        names = delimiter.split(expt_types)
        for name in names:
            name = self._custom_experiment_type_regexes(experiment, name)
            name = name.lower().strip()
            type_results = ExperimentType.objects.filter(type_name__iexact=name)
            # We don't see it in the db, so ask the user
            if not type_results:
                response = ''
                while not response or response not in "AaIi":
                    response = raw_input("Experiment type '%s' is not known by"
                                         " the database.  Would you like to "
                                         "[A]dd the type or [I]gnore it? " %
                                         name)

                if response in "Aa":
                    exp_type = ExperimentType(type_name=name)
                    exp_type.save()
                else:
                    continue
            elif len(type_results) > 1:
                print ("Warning: More than one match for experiment type "
                       "'%s':\n%s\nUsing first result." % (name, type_results))
                exp_type = type_results[0]
            else:
                exp_type = type_results[0]
            experiment.expt_type.add(exp_type)
            experiment.save()

    def add_transcription_factors(self, experiment, tf_names):
        """
        Takes string of transcription factors, splits them, and ensures that
        the are valid and extant. Asks user to confirm addition of new type if
        not.  This is a lot of duplicated code from add_experiment_types, but
        it had a few too many differences to easily abstract them out.
        """
        delimiter = re.compile('\s*[/;,+&]+\s*')
        names = delimiter.split(tf_names)
        for name in names:
            name = self._custom_transcription_factor_regexes(experiment, name)
            name = name.lower().strip()
            tf_results = TranscriptionFactor.objects.filter(tf__iexact=name)
            if not tf_results:
                response = ''
                while not response or response not in "AaIi":
                    response = raw_input("Transcription factor '%s' is not"
                                         " known by the database.  Would you "
                                         "like to [A]dd the type or [I]gnore "
                                         "it? " % name)

                if response in "Aa":
                    tf = TranscriptionFactor(tf=name)
                    tf.save()
                else:
                    continue
            elif len(tf_results) > 1:
                print ("Warning: More than one match for transcription factor "
                       "'%s':\n%s\nUsing first result." % (name, type_results))
                tf = tf_results[0]
            else:
                tf = tf_results[0]
            experiment.transcription_factor.add(tf)
            experiment.save()

    def _validate_row(self, row):
        """
        Perform basic validation of the data in the row.
        """
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
        return row

    def _custom_experiment_type_regexes(self, experiment, expt_type):
        """
        Fix mistakes that we've seen in the data so far.
        """
        # Sometimes they forget the dash in experiment names
        expt_type = re.sub('qPCR', 'q-PCR', expt_type, flags=re.I)
        expt_type = re.sub('Run on', 'run-on', expt_type, flags=re.I)
        expt_type = re.sub('run off', 'run-off', expt_type, flags=re.I)
        # Found this typo in the data.  We can fix it for them.
        expt_type = re.sub('Westernn', 'Western', expt_type, flags=re.I)
        return expt_type

    def _custom_transcription_factor_regexes(self, experiment, tf):
        # This one isn't supposed to have a dash
        tf = re.sub('NF-kB', 'NFkB', tf, flags=re.I)
        # The data they give us may have Myc transcription factors as just
        # the letter for the family member.  We fix that here.
        if (experiment.transcription_family == Experiment.MYC and
            Experiment.MYC.lower() not in tf.lower()):
            tf = re.sub('(.*)', r'Myc-\1', tf, flags=re.I)
        # The data they give us may have STAT transcription factors as just
        # the digit for the family member.  We fix that here.
        if (experiment.transcription_family == Experiment.STAT and
            Experiment.STAT.lower() not in tf.lower()):
            tf = re.sub('(.*)', r'STAT\1', tf, flags=re.I)
        return tf
