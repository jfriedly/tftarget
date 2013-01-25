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
            r = reader.next()
            for row in reader:
                e = Experiment()
                e.save()
