# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SortChannel'
        db.create_table('sturnus_sortchannel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recording_channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sturnus.RecordingChannel'])),
            ('sort', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sturnus.Sort'])),
            ('threshold_upper', self.gf('django.db.models.fields.FloatField')(default=2.5)),
            ('threshold_lower', self.gf('django.db.models.fields.FloatField')(default=-2.5)),
        ))
        db.send_create_signal('sturnus', ['SortChannel'])

        # Adding model 'Sort'
        db.create_table('sturnus_sort', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sturnus', ['Sort'])

        # Adding M2M table for field trials on 'Sort'
        db.create_table('sturnus_sort_trials', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sort', models.ForeignKey(orm['sturnus.sort'], null=False)),
            ('trial', models.ForeignKey(orm['sturnus.trial'], null=False))
        ))
        db.create_unique('sturnus_sort_trials', ['sort_id', 'trial_id'])


    def backwards(self, orm):
        # Deleting model 'SortChannel'
        db.delete_table('sturnus_sortchannel')

        # Deleting model 'Sort'
        db.delete_table('sturnus_sort')

        # Removing M2M table for field trials on 'Sort'
        db.delete_table('sturnus_sort_trials')


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
        'sturnus.electrode': {
            'Meta': {'object_name': 'Electrode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sturnus.electrodemodel': {
            'Meta': {'object_name': 'ElectrodeModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'model_number': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sturnus.electrodepad': {
            'Meta': {'object_name': 'ElectrodePad'},
            'electrode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.Electrode']"}),
            'electrode_pad_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.ElectrodePadModel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impedance': ('django.db.models.fields.FloatField', [], {'null': 'True'})
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
        'sturnus.penetration': {
            'Meta': {'object_name': 'Penetration'},
            'alpha_angle': ('django.db.models.fields.FloatField', [], {'default': '90'}),
            'beta_angle': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'depth_max': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hemisphere': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lateral': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rostral': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rotation_angle': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'sturnus.recordingchannel': {
            'Meta': {'unique_together': "(('site', 'pad'),)", 'object_name': 'RecordingChannel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.ElectrodePad']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.Region']", 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.Site']"})
        },
        'sturnus.region': {
            'Meta': {'object_name': 'Region'},
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_part_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.Region']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'sturnus.site': {
            'Meta': {'object_name': 'Site'},
            'blocks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sturnus.Block']", 'symmetrical': 'False'}),
            'depth': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'penetration': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.Penetration']"})
        },
        'sturnus.sort': {
            'Meta': {'object_name': 'Sort'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recording_channels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sturnus.RecordingChannel']", 'through': "orm['sturnus.SortChannel']", 'symmetrical': 'False'}),
            'trials': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sturnus.Trial']", 'symmetrical': 'False'})
        },
        'sturnus.sortchannel': {
            'Meta': {'object_name': 'SortChannel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recording_channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.RecordingChannel']"}),
            'sort': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sturnus.Sort']"}),
            'threshold_lower': ('django.db.models.fields.FloatField', [], {'default': '-2.5'}),
            'threshold_upper': ('django.db.models.fields.FloatField', [], {'default': '2.5'})
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