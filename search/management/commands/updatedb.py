from django.core.management.base import BaseCommand, CommandError
import csv

from search.models import Experiment, Transcription, Tissue

class Command(BaseCommand):
    args = 'filename'
    help = ("Updates the database with new rows from a CSV file.\n\n"
            "The CSV file should use tab characters to separate values.\n"
            "You can create a CSV in Excel by using 'Save as...' and\n"
            "selecting .csv or by using 'Export'.\n")

    def handle(self, *args, **options):
        # This is the expected order of columns. It can easily be re-arranged.
        columns = ['gene', 'transcription_family', 'pmid', 'species',
                'experimental_tissues', 'cell_line',
                'expt_name', 'replicates', 'control', 'quality']
        if len(args) != 1:
            raise CommandError("Please give one and only one filename.")
        #(jfriedly) I considered putting this in a try: except IOError, but I
        # think it's better to just let that bubble up.
        with open(args[0], 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=columns, delimiter='\t')
            # Skip the first row (column names)
            r = reader.next()
            for row in reader:
                expt_names = row.pop('expt_name')
                e = Experiment(**row)
                e.save()
                add_experiment_types(e, expt_names)

    def check_expts(experiment, expt_names):
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
            exp_type = Experiment.objects.get(type_name__contains=name)
            print exp_type
            if not exp_type:  # We don't see it in the db, so ask the user
                print "Experiment type %s is not known by the database. Would"
                    "you like to [A]dd the type or [I]gnore it?"
                response = ''
                while response not in "AaIi":
                    response = raw_input()

                if response == "A" or "a":
                    exp_type = Experiment_Type(experiment)
                    exp_type.save()
                else:
                    continue
            experiment.expt_name.add(name)

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
