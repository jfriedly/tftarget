from django.core.management.base import BaseCommand, CommandError
from search._constants import ALL_SPECIES
from search.models import Gene
from django.db.models import Q
import csv
import sys
import operator


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

                # Ignore empty cells
                for species in row.keys():
                    if not row[species]:
                        row.pop(species)

                # Select where any of the given values are present
                query = reduce(operator.or_, (Q(**{s:g}) for s, g in row.iteritems()))
                gene = Gene.objects.filter(query)

                # Modify extant entry or create a new one.
                if gene:
                    #FIXME This works when only two columns are actually in use,
                    # but there is the potential for data loss if more columns
                    # are used later on.
                    # Remove duplicates, if there are any.
                    if len(gene) > 1:
                        for g in gene:
                            g.delete()
                    #Perform the modification.
                    dupes += 1
                    gene = gene[0]
                    for species in row.keys():
                        gene.__setattr__(species, row[species])
                    gene.save()
                else:
                    adds += 1
                    gene = Gene(**row)
                    gene.save()

            print ('\nAdded %d/%d entries and modified %d. Ignored %d errors.'
                    % (adds, adds+dupes+errors, dupes, errors))
