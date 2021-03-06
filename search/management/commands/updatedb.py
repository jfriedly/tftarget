from django.core.management.base import BaseCommand, CommandError
import csv
import re
import sys
from copy import deepcopy
from search._constants import (TFS,
                               ALL_SPECIES,
                               IMPORT_COLUMN_ORDER,
                               EXPT_TYPES,
                               ALL_TISSUES)


from search.models import Experiment, Gene
from search.management.commands._shared import DBImportError


# We use this a lot, so we should only compile it once.
DELIMITER = re.compile('\s*[/;,&]+\s*')


class Command(BaseCommand):
    args = 'filename'
    help = ("Updates the database with new rows from a CSV file.\n\n"
            "The CSV file should use tab characters to separate values.\n"
            "You can create a CSV in Excel by using 'Save as...' and\n"
            "selecting .csv or by using 'Export'.\n")

    def handle(self, *args, **options):
        """Main function of the management command.  When the management
        command is called from a shell, this function 'handles' it.
        """
        columns = IMPORT_COLUMN_ORDER
        if len(args) != 1:
            raise CommandError("Please give one and only one filename.")

        logfile = args[0] + '.log'
        with open(args[0], 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=columns,
                                    delimiter='\t')
            # Skip the first row (column names)
            r = reader.next()
            # But check it to make sure the user is at least *trying* to get
            # the right number of columns.
            if not all((r[c] for c in columns)):
                print ('This file is missing some columns. This may be due to '
                       'saving the file in an incorrect format. Please fix '
                       'this, and try again.')
                return

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

                # Try to validate, then add the row. If it doesn't work, say so
                # and increment the error counter.
                try:
                    row = self._validate(row, line)
                    added, dupe = self._add(row, line)
                    adds += added
                    dupes += dupe
                except DBImportError as e:
                    errors += 1
                    sys.stdout.write('\n%s\n%s line:      ' % (e, args[0]))
                    with open(logfile, 'a') as log:
                        log.write('\n%s' % e)

            # We're done, so print out the summary.
            done = ('\nAdded %d/%d entries. Ignored %d errors and %d duplicates.'
                    % (adds, adds + dupes + errors, errors, dupes))
            print done
            with open(logfile, 'a') as log:
                log.write(done)

    def _split_cell(self, row, name, depth, line):
        """
        Split a cell into multiple values if they can be found and return them
        as well as the 'depth'.  The 'depth' is the index for which value we're
        currently parsing.

        If depth comes in as 1 and the number of values parsed is > 1, then
        return the total depth.  If depth comes in as something other than 1,
        return whatever it was before.
        """
        cell_values = DELIMITER.split(row)
        if len(cell_values) > 1:
            if (depth > 1 and len(cell_values) != depth):
                raise DBImportError(
                    "Error on line %d: Number of row sub-values does not "
                    "match in each column. %s has %d values, while previous "
                    "columns had %d values." % (line, name, len(cell_values),
                                                depth))
            depth = len(cell_values)
        return cell_values, depth

    def _validate(self, row, line):
        """
        Preform basic row validation before adding the row in.
        """
        species = row['species'].strip().lower()
        if species not in ALL_SPECIES:
            if len(DELIMITER.split(species)) > 1:
                raise DBImportError("Error on line %d: Species %s is not valid."
                                    " You may have put more than one species"
                                    " in the same cell. This is not supported."
                                    % (line, species))
            else:
                raise DBImportError("Error on line %d: Species %s is not valid."
                                    % (line, species))
        row['species'] = species

        # Let's just make sure nobody's being clever with genes here.
        gene = row['gene'][:255]
        if len(DELIMITER.split(gene)) > 1:
            raise DBImportError("Error on line %d: There appear to be multiple"
                                " genes on one row. This is not supported. The"
                                " given value was %s" % (line, gene))
        #If more ortholog species are added, this section will need to be
        #changed to reflect that. You may end up wanting to use something like
        #get_or_create(**{species: gene}) for that...
        if species == 'mouse':
            gene, created = Gene.objects.get_or_create(mouse=gene)
        else:
            gene, created = Gene.objects.get_or_create(human=gene)
        row['gene'] = gene

        # Give an error for multiple PMIDs on a row
        pmid = row['pmid'][:255].lower() or ''
        if len(DELIMITER.split(pmid)) > 1:
            raise DBImportError("Error on line %d: There appear to be multiple"
                                " PMIDs on one row. This is not supported. The"
                                " given value was %s" % (line, pmid))
        # Make sure pmid can be made an int, but pass on empty strings.
        if pmid and pmid not in ('na', 'n/a'):
            try:
                int(row['pmid'])
            except ValueError:
                raise DBImportError("Error on line %d: PMID must be a valid"
                                    "integer. Got '%s'" % (line, row['pmid']))
        else:
            row['pmid'] = None

        #Capitalize the organ value
        if not row['expt_tissues']:
            row['expt_tissues'] = ''
        else:
            organ = row['expt_tissues'][:255].lower().replace(' ', '')
            if organ in ('na', 'n/a', 'n-a'):
                organ = 'na'
            elif organ not in ALL_TISSUES:
                raise DBImportError('Error on line %d: Experiment tissue %s '
                                    'is not valid.' % (line,
                                                       row['expt_tissues']))
            row['expt_tissues'] = ALL_TISSUES[organ]

        #Validate the rest of the values
        if not row['replicates']:
            row['replicates'] = ''
        else:
            row['replicates'] = row['replicates'][:50]

        if not row['control']:
            row['control'] = ''
        else:
            row['control'] = row['control'][:255]

        if not row['quality']:
            row['quality'] = ''
            row['quality_factor'] = 1
        else:
            row['quality'] = row['quality'][:255]
            factor = -1.5
            for q in DELIMITER.split(row['quality']):
                q = q.lower().strip()
                try:
                    factor = float(q)
                    break
                except:
                    if q in ['high', 'h']:
                        factor = 3
                    elif q in ['med', 'medium', 'm']:
                        factor = 2
                    elif q in ['low', 'l']:
                        factor = 1
            factor = abs(factor)
            if factor < 1.5:
                factor = 1
            elif factor > 2:
                factor = 3
            else:
                factor = 2
            row['quality_factor'] = factor
        return row

    def _get_row_multis(self, row, row_multis, key, name, depth, line, check_func):
        """For columns that can have multiple values, create the row_multis
        list of appropriate dicts.
        """
        data = row.pop(key)
        if not data:
            raise DBImportError("Error on line %d: No %s." %
                                (line, name.lower()))
        # Split up the row, and check that the depth is valid
        cell_values, depth = self._split_cell(data, name, depth, line)
        if len(cell_values) == 1:
            cell_values = cell_values * depth
        # If our list of multis is too short, grow it
        while len(row_multis) < depth:
            row_multis.append(deepcopy(row_multis[0]))
        # Then, add each cell value to a row_multi list of dicts
        for n, value in enumerate(cell_values):
            value = check_func(value, line)
            row_multis[n][key] = value
        return row_multis, depth

    def _add(self, row, line):
        """
        Add rows to the database intelligently, looking for delimited values.
        """
        # The number of delimited values in the row. Supposedly, for each column
        # this will be n where n == 1 or n is the same for all columns in row
        depth = 1
        row_multis = [{}]

        #NOTE only trans. fac, expt, cell line/organ can have multi-value
        #We define the function that each key should be checked against, and
        #send it on to the function that breaks up the cells. This way we can
        #check these things as we go. There's probably a better way.
        def validate_transcription_factor(value, line):
            canonical_value = TFS.get(value.translate(None, '-_. ').lower())
            if not canonical_value:
                raise DBImportError("Error on line %d: Transcription factor %s"
                                    " is not valid." % (line, value))
            return canonical_value
        row_multis, depth = self._get_row_multis(row, row_multis,
                                                 'transcription_factor',
                                                 'Transcription factor',
                                                 depth, line,
                                                 validate_transcription_factor)

        def validate_cell_line(value, line):
            return value
        row_multis, depth = self._get_row_multis(row, row_multis, 'cell_line',
                                                 'Cell line', depth, line,
                                                 validate_cell_line)

        def validate_expt_type(value, line):
            canonical_value = EXPT_TYPES.get(value.translate(None, '-_. ').lower())
            if not canonical_value:
                raise DBImportError("Error on line %d: Experiment type %s"
                                    " is not valid." % (line, value))
            return canonical_value
        row_multis, depth = self._get_row_multis(row, row_multis, 'expt_type',
                                                 'Experiment type', depth,
                                                 line, validate_expt_type)

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
