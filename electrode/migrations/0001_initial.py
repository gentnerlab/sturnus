# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ElectrodeModel'
        db.create_table(u'electrode_electrodemodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('model_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'electrode', ['ElectrodeModel'])

        # Adding model 'RecordingSiteModel'
        db.create_table(u'electrode_recordingsitemodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('electrode_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['electrode.ElectrodeModel'])),
            ('connector_chan', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('size', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('size_units', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('x_coord', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('y_coord', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('z_coord', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'electrode', ['RecordingSiteModel'])

        # Adding model 'Electrode'
        db.create_table(u'electrode_electrode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('arrival_date', self.gf('django.db.models.fields.DateField')()),
            ('uses', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('electrode_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['electrode.ElectrodeModel'])),
        ))
        db.send_create_signal(u'electrode', ['Electrode'])

        # Adding model 'RecordingSite'
        db.create_table(u'electrode_recordingsite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('impedance', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('electrode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['electrode.Electrode'])),
            ('electrode_pad_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['electrode.RecordingSiteModel'])),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'electrode', ['RecordingSite'])

        # Adding model 'RecChan'
        db.create_table(u'electrode_recchan', (
            (u'recordingchannel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['django_neo.RecordingChannel'], unique=True, primary_key=True)),
            ('chan', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('gain', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('filter_high', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('filter_low', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['electrode.RecordingSite'])),
        ))
        db.send_create_signal(u'electrode', ['RecChan'])


    def backwards(self, orm):
        # Deleting model 'ElectrodeModel'
        db.delete_table(u'electrode_electrodemodel')

        # Deleting model 'RecordingSiteModel'
        db.delete_table(u'electrode_recordingsitemodel')

        # Deleting model 'Electrode'
        db.delete_table(u'electrode_electrode')

        # Deleting model 'RecordingSite'
        db.delete_table(u'electrode_recordingsite')

        # Deleting model 'RecChan'
        db.delete_table(u'electrode_recchan')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'django_neo.annotation': {
            'Meta': {'object_name': 'Annotation'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_neo.Attribute']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'django_neo.attribute': {
            'Meta': {'object_name': 'Attribute'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'django_neo.recordingchannel': {
            'Meta': {'object_name': 'RecordingChannel'},
            'coord_units': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file_origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'x_coord': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_coord': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z_coord': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'electrode.electrode': {
            'Meta': {'object_name': 'Electrode'},
            'arrival_date': ('django.db.models.fields.DateField', [], {}),
            'electrode_model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['electrode.ElectrodeModel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'uses': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'electrode.electrodemodel': {
            'Meta': {'object_name': 'ElectrodeModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'model_number': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'electrode.recchan': {
            'Meta': {'object_name': 'RecChan', '_ormbases': [u'django_neo.RecordingChannel']},
            'chan': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'filter_high': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'filter_low': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gain': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            u'recordingchannel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['django_neo.RecordingChannel']", 'unique': 'True', 'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['electrode.RecordingSite']"})
        },
        u'electrode.recordingsite': {
            'Meta': {'object_name': 'RecordingSite'},
            'electrode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['electrode.Electrode']"}),
            'electrode_pad_model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['electrode.RecordingSiteModel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impedance': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'electrode.recordingsitemodel': {
            'Meta': {'object_name': 'RecordingSiteModel'},
            'connector_chan': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'electrode_model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['electrode.ElectrodeModel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'size_units': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'x_coord': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'y_coord': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'z_coord': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['electrode']