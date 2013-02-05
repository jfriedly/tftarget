from django.core.management.base import BaseCommand, CommandError
import csv
import re

from search.models import Experiment, Experiment_Type

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
                'expt_name', 'replicates', 'control', 'quality']
        if len(args) != 1:
            raise CommandError("Please give one and only one filename.")

        transcription_family = args[0].split('.')[0]
        families = {f[0].lower(): f[0] for f in Experiment.TF_FAMILIES}
        if not transcription_family.lower() in families:
            print ("Please make the name of your file the same as the"
                "transcription family of the factors in it. This will likely"
                "be the name of the worksheet you are exporting from.")
            return

        #(jfriedly) I considered putting this in a try: except IOError, but I
        # think it's better to just let that bubble up.
        with open(args[0], 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=columns, delimiter='\t')
            # Skip the first row (column names)
            r = reader.next()
            for row in reader:
                row['transcription_family'] = families[transcription_family]
                expt_names = row.pop('expt_name')
                e = Experiment(**row)
                e.save()
                self.add_experiment_types(e, expt_names)
                e.save()

    def add_experiment_types(self, experiment, expt_names):
        """
        Takes string of experiment types, splits them, and ensures that they are
        valid and extant. Asks user to confirm addition of new type if not.
        """
        delimiter = re.compile('\s*[;,+&]+\s*')
        # Matches one or more semicolon, comma, plus sign, and/or ampersand,
        # possibly with whitespace on either side.
        names = delimiter.split(expt_names)
        for name in names:
            name = name.lower()
            type_results = Experiment_Type.objects.filter(type_name__iexact=name)
            if not type_results:  # We don't see it in the db, so ask the user
                response = ''
                while not response or response not in "AaIi":
                    response = raw_input("Experiment type %s is not known by "
                                         "the database.  Would you like to "
                                         "[A]dd the type or [I]gnore it? " %
                                         name)

                if response in "Aa":
                    exp_type = Experiment_Type(type_name=name)
                    exp_type.save()
                else:
                    continue
            elif len(type_results) != 1:
                print ("Warning: More than one match for experiment type %s:\n"
                    "%s \n Using first result." % (name, type_results))
                exp_type = type_results[0]
            else:
                exp_type = type_results[0]
            experiment.expt_name.add(exp_type)
            experiment.save()

    def _valid_row(row):
        """
        Perform basic validation of the data in the row.
        """
        # Check for valid gene
        if not len(row['gene']) <= 255:
            return False

        # Make sure pmid can be made an int
        try:
            int(row['pmid'])
        except ValueError:
            return False
