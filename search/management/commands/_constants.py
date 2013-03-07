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


#NOTE Changing this is not the only step to add a new species! You must also
#add the column to the species table in models.py, and migrate the database.
ALL_SPECIES = ('human', 'mouse', 'rat', 'arabidopsis', 'hamster')
