# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field expt_name on 'Experiment'
        db.create_table('search_experiment_expt_name', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('experiment', models.ForeignKey(orm['search.experiment'], null=False)),
            ('experiment_type', models.ForeignKey(orm['search.experiment_type'], null=False))
        ))
        db.create_unique('search_experiment_expt_name', ['experiment_id', 'experiment_type_id'])


    def backwards(self, orm):
        # Removing M2M table for field expt_name on 'Experiment'
        db.delete_table('search_experiment_expt_name')


    models = {
        'search.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'cell_line': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'control': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'experimental_tissues': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'expt_name': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['search.Experiment_Type']", 'symmetrical': 'False'}),
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