# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Experiment_Type'
        db.create_table('search_experiment_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True)),
        ))
        db.send_create_signal('search', ['Experiment_Type'])

        # Deleting field 'Experiment.expt_name'
        db.delete_column('search_experiment', 'expt_name')


    def backwards(self, orm):
        # Deleting model 'Experiment_Type'
        db.delete_table('search_experiment_type')

        # Adding field 'Experiment.expt_name'
        db.add_column('search_experiment', 'expt_name',
                      self.gf('django.db.models.fields.CharField')(default='foo', max_length=255),
                      keep_default=False)


    models = {
        'search.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'cell_line': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'control': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'experimental_tissues': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'gene': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pmid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'quality': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True'}),
            'replicates': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'transcription_family': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'search.experiment_type': {
            'Meta': {'object_name': 'Experiment_Type'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'})
        },
        'search.tissue': {
            'Meta': {'object_name': 'Tissue'},
            'expt_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['search.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tissue_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'search.transcription': {
            'Meta': {'object_name': 'Transcription'},
            'expt_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['search.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transcription_factor': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['search']