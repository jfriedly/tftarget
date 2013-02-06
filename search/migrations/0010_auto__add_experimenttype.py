# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExperimentType'
        db.create_table('search_experimenttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True)),
        ))
        db.send_create_signal('search', ['ExperimentType'])

        # Adding M2M table for field expt_name on 'Experiment'
        db.create_table('search_experiment_expt_name', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('experiment', models.ForeignKey(orm['search.experiment'], null=False)),
            ('experimenttype', models.ForeignKey(orm['search.experimenttype'], null=False))
        ))
        db.create_unique('search_experiment_expt_name', ['experiment_id', 'experimenttype_id'])


    def backwards(self, orm):
        # Deleting model 'ExperimentType'
        db.delete_table('search_experimenttype')

        # Removing M2M table for field expt_name on 'Experiment'
        db.delete_table('search_experiment_expt_name')


    models = {
        'search.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'cell_line': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'control': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'experimental_tissues': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'expt_name': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['search.ExperimentType']", 'symmetrical': 'False'}),
            'gene': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pmid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'quality': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True'}),
            'replicates': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'transcription_factor': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['search.TranscriptionFactor']", 'symmetrical': 'False'}),
            'transcription_family': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'search.experimenttype': {
            'Meta': {'object_name': 'ExperimentType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'})
        },
        'search.transcriptionfactor': {
            'Meta': {'object_name': 'TranscriptionFactor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tf': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['search']