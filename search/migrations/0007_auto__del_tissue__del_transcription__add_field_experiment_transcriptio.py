# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Tissue'
        db.delete_table('search_tissue')

        # Deleting model 'Transcription'
        db.delete_table('search_transcription')

        # Adding field 'Experiment.transcription_factor'
        db.add_column('search_experiment', 'transcription_factor',
                      self.gf('django.db.models.fields.CharField')(default='e2f', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Tissue'
        db.create_table('search_tissue', (
            ('expt_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Experiment'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tissue_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('search', ['Tissue'])

        # Adding model 'Transcription'
        db.create_table('search_transcription', (
            ('expt_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Experiment'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transcription_factor', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True)),
        ))
        db.send_create_signal('search', ['Transcription'])

        # Deleting field 'Experiment.transcription_factor'
        db.delete_column('search_experiment', 'transcription_factor')


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
            'transcription_factor': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'transcription_family': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'search.experiment_type': {
            'Meta': {'object_name': 'Experiment_Type'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['search']