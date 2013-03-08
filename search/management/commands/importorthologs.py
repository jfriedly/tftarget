from django.core.management.base import BaseCommand, CommandError
from _constants import ALL_SPECIES
from search.models import Gene
import csv
import sys


class DBImportError(Exception):
    message = ''

    def __init__(self, message=None):
        if message:
            self.message = message
        super(DBImportError, self).__init__(self.message)


class Command(BaseCommand):
    args = 'filename'
    help = ("Updates the orthologs table in the database with new rows from a"
            "CSV file.")

    def handle(self, *args, **options):
        """Main function of the management command.  When the management
        command is called from a shell, this function 'handles' it.
        """

        if len(args) != 1:
            raise CommandError("Please give one and only one filename.")

        with open(args[0], 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=ALL_SPECIES,
                                    delimiter='\t')
            # Skip the first row (column names)
            r = reader.next()
            sys.stdout.write(args[0] + ' line:       ')
            errors = 0
            adds = 0
            dupes = 0
            for line, row in enumerate(reader, start=2):
                sys.stdout.write('\b' * 5 + str(line).rjust(5))
                sys.stdout.flush()
                # Sometimes the data has an extra column.  Ignore it.
                if row.has_key(None):
                    row.pop(None)
                values = dict()
                for key in row.keys():
                    if row[key]:
                        values[key] = row[key]
                g, created = Gene.objects.get_or_create(**values)
                if not created:
                    dupes += 1
                else:
                    adds += 1
            print ('\nAdded %d/%d entries. Ignored %d errors and %d duplicates.'
                    % (adds, adds+dupes+errors, errors, dupes))
