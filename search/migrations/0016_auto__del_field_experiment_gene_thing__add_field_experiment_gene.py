# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Experiment.gene_thing'
        db.delete_column('search_experiment', 'gene_thing_id')

        # Adding field 'Experiment.gene'
        db.add_column('search_experiment', 'gene',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Gene'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Experiment.gene_thing'
        db.add_column('search_experiment', 'gene_thing',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Gene'], null=True),
                      keep_default=False)

        # Deleting field 'Experiment.gene'
        db.delete_column('search_experiment', 'gene_id')


    models = {
        'search.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cell_line': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'control': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expt_tissues': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'expt_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'gene': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['search.Gene']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pmid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'quality': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'replicates': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'transcription_factor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'search.gene': {
            'Meta': {'object_name': 'Gene'},
            'arabidopsis': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'human': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mouse': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'rat': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['search']