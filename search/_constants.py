"""
This file contains valid data values for the importer. They are stored in a
dictionary, mapping the "slug" of the value - lower case, with all dashes,
punctuation, and spaces  stripped - to the "canonical" value - the one which
will actually display.
"""

ALL_TISSUES = {
    'na': 'N/A',
    'adrenalgland': 'Adrenal gland',
    'appendix': 'Appendix',
    'bladder': 'Bladder',
    'blood': 'Blood',
    'bone': 'Bone',
    'bonemarrow': 'Bone marrow',
    'brain': 'Brain',
    'breast': 'Breast',
    'cartilage': 'Cartilage',
    'embryo': 'Embryo',
    'esophagus': 'Esophagus',
    'eye': 'Eye',
    'gallbladder': 'Gall bladder',
    'heart': 'Heart',
    'kidney': 'Kidney',
    'largeintestine': 'Large intestine',
    'liver': 'Liver',
    'lung': 'Lung',
    'muscle': 'Muscle',
    'ovary': 'Ovary',
    'pancreas': 'Pancreas',
    'parathyroidgland': 'Parathyroid gland',
    'pinealgland': 'Pineal gland',
    'pituitarygland': 'Pituitary gland',
    'placenta': 'Placenta',
    'prostate': 'Prostate',
    'skin': 'Skin',
    'smallintestine': 'Small intestine',
    'spleen': 'Spleen',
    'stomach': 'Stomach',
    'testis': 'Testis',
    'thymmus': 'Thymus',
    'thyroidgland': 'Thyroid gland',
    'trachea': 'Trachea',
    'uterus': 'Uterus',
}

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
    'e2f3b': 'E2F3b',
    'e2f4': 'E2F4',
    'e2f5': 'E2F5',
    'e2f6': 'E2F6',
    'e2f7': 'E2F7',
    'e2f8': 'E2F8',

    #FOX
    'foxa': 'FOXA',
    'foxm': 'FOXM',
    'foxo': 'FOXO',
}


# Short name to make stuff pass pep8 easier
TFS = TRANSCRIPTION_FACTORS

# Genes for which the sum of (experiment weight * quality factor) across all
# experiments in which they were involved is less than this number will not be
# shown in a direct target search. 1, 2, and 3 are the possible quality factors
# (for low, medium, and high quality experiments respectively) and experiment
# weights are defined below.
DIRECT_SEARCH_THRESHOLD = 3

# This maps a slugified experiment name to a tuple of it's canonical
# (that is, capitalized) name, its relative weight in direct target searches,
# and it's category (currently binding or gene expression) for direct target
# searches
_experiments = {
    '': ('', 0, ''),
    'chip': ('ChIP', 1, 'binding'),
    'chipqpcr': ('ChIP-qPCR', 1, 'binding'),
    'chippcr': ('ChIP-PCR', 1, 'binding'),
    'chipchip': ('ChIP-chip', 1, 'binding'),
    'chipseq': ('ChIP-seq', 1, 'binding'),
    'emsa': ('EMSA', 1, 'binding'),
    'reportergeneassay': ('Reporter Gene Assay', 1, 'gene expression'),
    'westernblot': ('Western Blot', 1, 'gene expression'),
    'northernblot': ('Northern Blot', 1, 'gene expression'),
    'pcr': ('PCR', 1, 'gene expression'),
    'qpcr': ('q-PCR', 1, 'gene expression'),
    'rtpcr': ('RT-PCR', 1, 'gene expression'),
    'microarray': ('Microarray', 1, 'gene expression'),
    'rnaseq': ('RNA-seq', 1, 'gene expression'),
    'nuclearrunon': ('Nuclear run-on', 1, 'gene expression'),
    'nuclearrunoff': ('Nuclear run-off', 1, 'gene expression'),
}

EXPT_TYPES = {key: value[0] for key, value in _experiments.iteritems()}
EXPT_WEIGHTS = {name: weight for name, weight, cls in _experiments.itervalues()}
BINDING_EXPTS = set()
EXPRESSION_EXPTS = set()
for expt in _experiments.itervalues():
    if expt[2] == 'binding':
        BINDING_EXPTS.add(expt[0])
    elif expt[2] == 'gene expression':
        EXPRESSION_EXPTS.add(expt[0])

# The oder of columns in the database import file. You can re-arrange the order
# here, and things should "just work", but obviously adding more columns won't.
IMPORT_COLUMN_ORDER = ['gene', 'transcription_factor', 'pmid', 'species',
                       'expt_tissues', 'cell_line', 'expt_type', 'replicates',
                       'control', 'quality']

#NOTE Changing this is not the only step to add a new species! If you have
# orthologs, you must also add the species to the Gene table in models.py.
ALL_SPECIES = ('mouse', 'human', 'rat', 'arabidopsis', 'hamster', 'pig')


# Options for the search form
EMPTY_STRING = ''
TF_CHOICES = [
    ['E2F'] + [v for v in TFS.itervalues() if v.startswith('E2F')],
    # There's duplicates in here
    ['MYC'] + list(set([v for v in TFS.itervalues() if v[2:] == 'Myc'])),
    ['NFkB'] + [v for v in TFS.itervalues() if v.startswith('NF-kB')],
    ['FOX'] + [v for v in TFS.itervalues() if v.startswith('FOX')],
    ['STAT'] + [v for v in TFS.itervalues() if v.startswith('STAT')],
]
SPECIES_CHOICES = ([(EMPTY_STRING, EMPTY_STRING)] +
                   [(s.capitalize(), s.capitalize()) for s in ALL_SPECIES])
EXPT_CHOICES = [(v, v) for v in EXPT_TYPES.values()]
TISSUE_CHOICES = [(v, v) for v in ALL_TISSUES.values()]
# .sort() doesn't have a return value, so this actually sorts the lists
[sublist.sort() for sublist in TF_CHOICES]
EXPT_CHOICES.sort(key=lambda x: x[0])
TISSUE_CHOICES.sort(key=lambda x: x[0])
