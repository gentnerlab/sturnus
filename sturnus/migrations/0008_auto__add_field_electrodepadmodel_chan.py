# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ElectrodePadModel.chan'
        db.add_column('sturnus_electrodepadmodel', 'chan',
                      self.gf('django.db.models.fields.CharField')(default='ref', max_length=3),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ElectrodePadModel.chan'
        db.delete_column('sturnus_electrodepadmodel', 'chan')


    models = {
        'sturnus.behaviortrial': {
            'Meta': {'object_name': 'BehaviorTrial', '_ormbases': ['sturnus.Trial']},
            'cum_correct': ('django.db.models.fields.IntegerField', [], {}),
            'cum_correct_thresh': ('django.db.models.fields.IntegerField', [], {}),
            'feed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'response': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'timeout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tr_class': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'tr_type': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'trial_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sturnus.Trial']", 'unique': 'True', 'primary_key': 'True'})
        },
        'sturnus.block': {
            'Meta': {'object_name': 'Block'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.Subject']"}),
            'title': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        'sturnus.electrodemodel': {
            'Meta': {'object_name': 'ElectrodeModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'model_number': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sturnus.electrodepadmodel': {
            'Meta': {'object_name': 'ElectrodePadModel'},
            'chan': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'electrode_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.ElectrodeModel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'x_coord': ('django.db.models.fields.IntegerField', [], {}),
            'y_coord': ('django.db.models.fields.IntegerField', [], {})
        },
        'sturnus.epoch': {
            'Meta': {'object_name': 'Epoch'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'epoch_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.EpochType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.Trial']"})
        },
        'sturnus.epochtype': {
            'Meta': {'object_name': 'EpochType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'sturnus.event': {
            'Meta': {'object_name': 'Event'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.EventType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.Trial']"})
        },
        'sturnus.eventtype': {
            'Meta': {'object_name': 'EventType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'sturnus.stimulus': {
            'Meta': {'object_name': 'Stimulus'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sturnus.subject': {
            'Meta': {'object_name': 'Subject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'})
        },
        'sturnus.trial': {
            'Meta': {'unique_together': "(('block', 'datetime'), ('block', 'tr_num'))", 'object_name': 'Trial'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.Block']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tr_num': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['sturnus']