import json

from django.db import models


class ExperimentType(models.Model):
    """Stores the experiment types as a many to many relation because an
    experiment can have multiple types.
    """
    EMPTY_STRING = ''
    CHIP = 'ChIP'
    CHIP_QPCR = 'ChIP-qPCR'
    CHIP_PCR = 'ChIP-PCR'
    CHIP_CHIP = 'ChIP-chip'
    CHIP_SEQ = 'ChIP-seq'
    EMSA = 'EMSA'
    REPORTER_GENE_ASSAY = 'Reporter Gene Assay'
    WESTERN_BLOT = 'Western Blot'
    NORTHERN_BLOT = 'Northern Blot'
    PCR = 'PCR'
    Q_PCR = 'q-PCR'
    RT_PCR = 'RT-PCR'
    MICROARRAY = 'Microarray'
    RNA_SEQ = 'RNA-seq'
    NUCLEAR_RUN_ON = 'Nuclearn run-on'
    NUCLEAR_RUN_OFF = 'Nuclearn run-off'
    EXPERIMENT_TYPES = ((EMPTY_STRING, EMPTY_STRING),
                        (CHIP, CHIP),
                        (CHIP_QPCR, CHIP_QPCR),
                        (CHIP_PCR, CHIP_PCR),
                        (CHIP_CHIP, CHIP_CHIP),
                        (CHIP_SEQ, CHIP_SEQ),
                        (EMSA, EMSA),
                        (REPORTER_GENE_ASSAY, REPORTER_GENE_ASSAY),
                        (WESTERN_BLOT, WESTERN_BLOT),
                        (NORTHERN_BLOT, NORTHERN_BLOT),
                        (PCR, PCR),
                        (Q_PCR, Q_PCR),
                        (RT_PCR, RT_PCR),
                        (MICROARRAY, MICROARRAY),
                        (RNA_SEQ, RNA_SEQ),
                        (NUCLEAR_RUN_ON, NUCLEAR_RUN_ON),
                        (NUCLEAR_RUN_OFF, NUCLEAR_RUN_OFF))
    BINDING_EXPTS = [CHIP, CHIP_QPCR, CHIP_PCR, CHIP_CHIP, CHIP_SEQ, EMSA]
    GENE_EXPRESSION_EXPTS = [REPORTER_GENE_ASSAY, WESTERN_BLOT, NORTHERN_BLOT,
                             PCR, Q_PCR, RT_PCR, MICROARRAY, RNA_SEQ,
                             NUCLEAR_RUN_ON, NUCLEAR_RUN_OFF]
    ALL_EXPTS = BINDING_EXPTS + GENE_EXPRESSION_EXPTS

    type_name = models.CharField(max_length=255, default='', null=True,
                                 choices=EXPERIMENT_TYPES)

    def __repr__(self):
        return "<ExperimentType: %s>" % self.type_name


class TranscriptionFactor(models.Model):
    """Stores the transcription factors as a many to many relation because an
    experiment can investigate multiple different factors.
    """
    NF_KB1 = 'NF-kB1'
    NF_KB2 = 'NF-kB2'
    NFKB_TFS = [NF_KB1, NF_KB2]

    STAT1 = 'STAT1'
    STAT1A = 'STAT1a'
    STAT3 = 'STAT3'
    STAT4 = 'STAT4'
    STAT5 = 'STAT5'
    STAT5A = 'STAT5a'
    STAT5B = 'STAT5b'
    STAT6 = 'STAT6'
    STAT_TFS = [STAT1, STAT1A, STAT3, STAT4, STAT5, STAT5A, STAT5B, STAT6]

    C_MYC = 'c-Myc'
    N_MYC = 'n-Myc'
    MYC_TFS = [C_MYC, N_MYC]

    E2F1 = 'E2F1'
    E2F2 = 'E2F2'
    E2F3 = 'E2F3'
    E2F3A = 'E2F3a'
    E2F4 = 'E2F4'
    E2F5 = 'E2F5'
    E2F6 = 'E2F6'
    E2F7 = 'E2F7'
    E2F_TFS = [E2F1, E2F2, E2F3, E2F3A, E2F4, E2F5, E2F6, E2F7]

    FOXA = 'FOXA'
    FOXM = 'FOXM'
    FOXO = 'FOXO'
    FOX_TFS = [FOXA, FOXM, FOXO]

    ALL_TFS = NFKB_TFS + STAT_TFS + MYC_TFS + E2F_TFS + FOX_TFS

    tf = models.CharField(max_length=255, null=True)

    def __repr__(self):
        return "<TranscriptionFactor: %s>" % self.tf


class Experiment(models.Model):
    """Stores data about each known experiment."""
    #TODO(jfriedly): We need to inspect the DB to figure out the options
    # for these
    EMPTY_STRING = ''
    E2F = 'E2F'
    MYC = 'Myc'
    NFKB = 'NFkB'
    FOX = 'FOX'
    STAT = 'STAT'
    TF_FAMILIES = ((EMPTY_STRING, EMPTY_STRING),
                   (E2F, E2F),
                   (MYC, MYC),
                   (NFKB, NFKB),
                   (FOX, FOX),
                   (STAT, STAT))
    HUMAN = 'Human'
    MOUSE = 'Mouse'
    RAT = 'Rat'
    ARABIDOPSIS = 'Arabidopsis'
    SPECIES = ((EMPTY_STRING, EMPTY_STRING),
               (HUMAN, HUMAN),
               (MOUSE, MOUSE),
               (RAT, RAT),
               (ARABIDOPSIS, ARABIDOPSIS))

    gene = models.CharField(max_length=255, default='', null=True)
    pmid = models.IntegerField(null=True)
    transcription_family = models.CharField(max_length=50, choices=TF_FAMILIES)
    transcription_factor = models.ManyToManyField(TranscriptionFactor)
    species = models.CharField(max_length=255, choices=SPECIES)
    expt_tissues = models.CharField(max_length=255, null=True)
    cell_line = models.CharField(max_length=255)
    expt_type = models.ManyToManyField(ExperimentType)
    replicates = models.CharField(max_length=50, default='', null=True)
    control = models.CharField(max_length=255, default='', null=True)
    quality = models.CharField(max_length=255, default='', null=True)

    def serialize(self):
        d = self.__dict__.copy()
        if '_state' in d:
            d.pop('_state')
        return d

    def __repr__(self):
        return json.dumps(self.serialize())
