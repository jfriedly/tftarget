"""
This file contains a command to import a spreadsheet of orthologs. It can
handle any arbitrary number of species in the import sheet (even though only
two are currently used) as long as they are in the order specified by the
ALL_SPECIES value in _constants and the appropriate tables have been added to
the Gene table. If species are added, you'll also need to change the front end
appropriately. It'll be a lot of work, but none of it in here.
"""
from django.core.management.base import BaseCommand, CommandError
from search._constants import ALL_SPECIES
from search.models import Gene, Experiment
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
                if None in row:
                    row.pop(None)

                # Ignore empty cells
                for species in row.keys():
                    if not row[species]:
                        row.pop(species)

                # Select where any of the given values are present
                query = reduce(operator.or_,
                               (Q(**{s: g}) for s, g in row.iteritems()))
                matches = Gene.objects.filter(query)

                # Modify extant entry or create a new one.
                if matches:
                    # The first result will become our final gene, and the rest
                    # will be assimilated and removed
                    gene = matches[0]
                    matches = matches[1:]
                    for match in matches:
                        # For each species, if the match has an ortholog,
                        # add it to the final gene
                        for species in ALL_SPECIES:
                            gene_name = match.__dict__[species]
                            if gene_name:
                                gene.__setattr__(species, gene_name)
                        # Then, reassociate all the experiments to the 
                        # final gene.
                        for exp in Experiment.objects.filter(gene=match):
                            exp.gene = gene
                            exp.save()
                        # And finally, delete the duplicate
                        match.delete()
                    # Lastly, add the values in the file to the final gene and
                    # save.
                    dupes += 1
                    for species in row.keys():
                        gene.__setattr__(species, row[species])
                    gene.save()
                else:
                    adds += 1
                    gene = Gene(**row)
                    gene.save()

            print ('\nAdded %d/%d entries and modified %d. Ignored %d errors.'
                   % (adds, adds + dupes + errors, dupes, errors))
