
import json

from django.db import models

class Gene(models.Model):
    human = models.CharField(max_length=255, default='', null=True)
    mouse = models.CharField(max_length=255, default='', null=True)
    rat = models.CharField(max_length=255, default='', null=True)
    arabidopsis = models.CharField(max_length=255, default='', null=True)
    hamster = models.CharField(max_length=255, default='', null=True)

    def serialize(self):
        d = self.__dict__.copy()
        if '_state' in d:
            d.pop('_state')
        return d

    def __repr__(self):
        return json.dumps(self.serialize())

class Experiment(models.Model):
    """Stores data about each known experiment."""
    gene = models.ForeignKey(Gene, null=True)
    pmid = models.IntegerField(null=True)
    transcription_factor = models.CharField(max_length=255, null=True)
    species = models.CharField(max_length=255)
    expt_tissues = models.CharField(max_length=255, null=True)
    cell_line = models.CharField(max_length=255)
    expt_type = models.CharField(max_length=255, default='', null=True)
    replicates = models.CharField(max_length=50, default='', null=True)
    control = models.CharField(max_length=255, default='', null=True)
    quality = models.CharField(max_length=255, default='', null=True)
    quality_factor = models.FloatField(default=-1.2)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def serialize(self, csv=False):
        d = self.__dict__.copy()
        if '_state' in d:
            d.pop('_state')
        if '_gene_cache' in d:
            d.pop('_gene_cache')
        d['created'] = str(d['created'])
        d['modified'] = str(d['modified'])
        if csv is True:
            d['gene'] = "%s" % Gene.objects.get(id=d.pop('gene_id')).serialize()
        else:
            d['gene'] = Gene.objects.get(id=d.pop('gene_id')).serialize()
        return d

    def __repr__(self):
        return json.dumps(self.serialize())
