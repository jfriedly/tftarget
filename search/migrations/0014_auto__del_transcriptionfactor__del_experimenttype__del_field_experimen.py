# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TranscriptionFactor'
        db.delete_table('search_transcriptionfactor')

        # Deleting model 'ExperimentType'
        db.delete_table('search_experimenttype')

        # Deleting field 'Experiment.transcription_family'
        db.delete_column('search_experiment', 'transcription_family')

        # Adding field 'Experiment.transcription_factor'
        db.add_column('search_experiment', 'transcription_factor',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Adding field 'Experiment.expt_type'
        db.add_column('search_experiment', 'expt_type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True),
                      keep_default=False)

        # Adding field 'Experiment.active'
        db.add_column('search_experiment', 'active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Experiment.created'
        db.add_column('search_experiment', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Experiment.modified'
        db.add_column('search_experiment', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field expt_type on 'Experiment'
        db.delete_table('search_experiment_expt_type')

        # Removing M2M table for field transcription_factor on 'Experiment'
        db.delete_table('search_experiment_transcription_factor')


    def backwards(self, orm):
        # Adding model 'TranscriptionFactor'
        db.create_table('search_transcriptionfactor', (
            ('tf', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('search', ['TranscriptionFactor'])

        # Adding model 'ExperimentType'
        db.create_table('search_experimenttype', (
            ('type_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('search', ['ExperimentType'])

        # Adding field 'Experiment.transcription_family'
        db.add_column('search_experiment', 'transcription_family',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=50),
                      keep_default=False)

        # Deleting field 'Experiment.transcription_factor'
        db.delete_column('search_experiment', 'transcription_factor')

        # Deleting field 'Experiment.expt_type'
        db.delete_column('search_experiment', 'expt_type')

        # Deleting field 'Experiment.active'
        db.delete_column('search_experiment', 'active')

        # Deleting field 'Experiment.created'
        db.delete_column('search_experiment', 'created')

        # Deleting field 'Experiment.modified'
        db.delete_column('search_experiment', 'modified')

        # Adding M2M table for field expt_type on 'Experiment'
        db.create_table('search_experiment_expt_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('experiment', models.ForeignKey(orm['search.experiment'], null=False)),
            ('experimenttype', models.ForeignKey(orm['search.experimenttype'], null=False))
        ))
        db.create_unique('search_experiment_expt_type', ['experiment_id', 'experimenttype_id'])

        # Adding M2M table for field transcription_factor on 'Experiment'
        db.create_table('search_experiment_transcription_factor', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('experiment', models.ForeignKey(orm['search.experiment'], null=False)),
            ('transcriptionfactor', models.ForeignKey(orm['search.transcriptionfactor'], null=False))
        ))
        db.create_unique('search_experiment_transcription_factor', ['experiment_id', 'transcriptionfactor_id'])


    models = {
        'search.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cell_line': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'control': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'expt_tissues': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'expt_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'gene': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'pmid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'quality': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'replicates': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'transcription_factor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['search']