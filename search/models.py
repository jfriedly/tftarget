import json

from django.db import models


class BaseModel():
    """Base model that other models inherit methods from."""

    def __repr__(self):
        d = self.__dict__
        if '_state' in d:
            d.pop('_state')
        return json.dumps(d)


class Experiment(BaseModel, models.Model):
    """Stores data about each known experiment."""
    gene = models.CharField(max_length=255, default='', null=True)
    pmid = models.IntegerField(null=True)
    transcription_family = models.CharField(max_length=50)
    species = models.CharField(max_length=255)
    experimental_tissues = models.CharField(max_length=255, null=True)
    cell_line = models.CharField(max_length=255)
    expt_name = models.ManyToManyField(Experiment_Type)
    replicates = models.CharField(max_length=50, default='', null=True)
    control = models.CharField(max_length=255, default='', null=True)
    quality = models.CharField(max_length=50, default='', null=True)


class Experiment_Type(BaseModel, models.Model):
    """Stores data about each known experiment type"""
    type_name = models.CharField(max_length=255, default='', null=True)

class Transcription(BaseModel, models.Model):
    """Relates transcription factors to experiments."""
    expt_id = models.ForeignKey(Experiment)
    transcription_factor = models.CharField(max_length=255, default='', null=True)


class Tissue(BaseModel, models.Model):
    """Relates tissues to experiments."""
    expt_id = models.ForeignKey(Experiment)
    tissue_name = models.CharField(max_length=255)
