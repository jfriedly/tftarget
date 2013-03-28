"""
This file contains valid data values for the importer. They are stored in a
dictionary, mapping the "slug" of the value - lower case, with all dashes and
punctuation stripped - to the "canonical" value - the one which will actually
display.
"""

TRANSCRIPTION_FACTORS = {
    #NF-kB
    'nfkb1': 'NF-kB1',
    'nfkb2': 'NF-kB2',

    #STAT
    'stat1': 'STAT1',
    'stat1a': 'STAT1a',
    'stat3': 'STAT3',
    'stat4': 'STAT4',
    'stat5': 'STAT5',
    'stat5a': 'STAT5a',
    'stat5b': 'STAT5b',
    'stat6': 'STAT6',

    #Myc
    'cmyc': 'c-Myc',
    'nmyc': 'n-Myc',
    'c': 'c-Myc',   # We've been told this is what to do with these values...
    'n': 'n-Myc',
    'myc': 'c-Myc',

    #E2F
    'e2f1': 'E2F1',
    'e2f2': 'E2F2',
    'e2f3': 'E2F3',
    'e2f3a': 'E2F3a',
    'e2f4': 'E2F4',
    'e2f5': 'E2F5',
    'e2f6': 'E2F6',
    'e2f7': 'E2F7',

    #FOX
    'foxa': 'FOXA',
    'foxm': 'FOXM',
    'foxo': 'FOXO',
}


# Short name to make stuff pass pep8 easier
TFS = TRANSCRIPTION_FACTORS


EXPT_TYPES = {
    '': '',
    'chip': 'ChIP',
    'chipqpcr': 'ChIP-qPCR',
    'chippcr': 'ChIP-PCR',
    'chipchip': 'ChIP-chip',
    'chipseq': 'ChIP-seq',
    'emsa': 'EMSA',
    'reportergeneassay': 'Reporter Gene Assay',
    'westernblot': 'Western Blot',
    'northernblot': 'Northern Blot',
    'pcr': 'PCR',
    'qpcr': 'q-PCR',
    'rtpcr': 'RT-PCR',
    'microarray': 'Microarray',
    'rnaseq': 'RNA-seq',
    'nuclearnrunon': 'Nuclearn run-on',
    'nuclearnrunoff': 'Nuclearn run-off',
}


# The oder of columns in the database import file. You can re-arrange the order
# here, and things should "just work", but obviously adding more columns won't.
IMPORT_COLUMN_ORDER = ['gene', 'transcription_factor', 'pmid', 'species',
                       'expt_tissues', 'cell_line', 'expt_type', 'replicates',
                       'control', 'quality']

#NOTE Changing this is not the only step to add a new species! You must also
#add the column to the species table in models.py, and migrate the database.
ALL_SPECIES = ('human', 'mouse', 'rat', 'arabidopsis', 'hamster')


# Options for the search form
EMPTY_STRING = ''
TF_CHOICES = [
    ['E2F'] + [v for v in TFS.values() if v.startswith('E2F')],
    ['MYC'] + [v for v in TFS.values() if v[2:] == 'Myc'],
    ['NFkB'] + [v for v in TFS.values() if v.startswith('NF-kB')],
    ['FOX'] + [v for v in TFS.values() if v.startswith('FOX')],
    ['STAT'] + [v for v in TFS.values() if v.startswith('STAT')],
]
SPECIES_CHOICES = ([(EMPTY_STRING, EMPTY_STRING)] +
                   [(s.capitalize(), s.capitalize()) for s in ALL_SPECIES])
EXPT_CHOICES = [(v, v) for v in EXPT_TYPES.values()]
