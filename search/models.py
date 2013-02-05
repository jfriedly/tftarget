import json

from django.db import models


class BaseModel():
    """Base model that other models inherit methods from."""

    def __repr__(self):
        d = self.__dict__
        if '_state' in d:
            d.pop('_state')
        return json.dumps(d)


class Experiment_Type(BaseModel, models.Model):
    """Stores data about each known experiment type"""
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
    type_name = models.CharField(max_length=255, default='', null=True,
                                 choices=EXPERIMENT_TYPES)


class Experiment(BaseModel, models.Model):
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
    transcription_factor = models.CharField(max_length=50)
    species = models.CharField(max_length=255, choices=SPECIES)
    experimental_tissues = models.CharField(max_length=255, null=True)
    cell_line = models.CharField(max_length=255)
    expt_name = models.ManyToManyField(Experiment_Type)
    replicates = models.CharField(max_length=50, default='', null=True)
    control = models.CharField(max_length=255, default='', null=True)
    quality = models.CharField(max_length=50, default='', null=True)
