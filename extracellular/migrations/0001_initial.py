# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CoordinateSystem'
        db.create_table(u'extracellular_coordinatesystem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'extracellular', ['CoordinateSystem'])

        # Adding model 'Penetration'
        db.create_table(u'extracellular_penetration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('file_origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('annotations', self.gf('djorm_hstore.fields.DictionaryField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('hemisphere', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('rostral', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('lateral', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('alpha_angle', self.gf('django.db.models.fields.FloatField')(default=90)),
            ('beta_angle', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('rotation_angle', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('depth_max', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('electrode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['electrode.Electrode'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['husbandry.Subject'])),
        ))
        db.send_create_signal(u'extracellular', ['Penetration'])

        # Adding model 'Location'
        db.create_table(u'extracellular_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('file_origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('annotations', self.gf('djorm_hstore.fields.DictionaryField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('penetration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['extracellular.Penetration'])),
            ('depth', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'extracellular', ['Location'])

        # Adding M2M table for field blocks on 'Location'
        m2m_table_name = db.shorten_name(u'extracellular_location_blocks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('location', models.ForeignKey(orm[u'extracellular.location'], null=False)),
            ('block', models.ForeignKey(orm[u'broab.block'], null=False))
        ))
        db.create_unique(m2m_table_name, ['location_id', 'block_id'])

        # Adding model 'ExtendedUnit'
        db.create_table(u'extracellular_extendedunit', (
            (u'unit_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['broab.Unit'], unique=True, primary_key=True)),
            ('quality', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('quality_method', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('multi', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'extracellular', ['ExtendedUnit'])

        # Adding model 'Popultaion'
        db.create_table(u'extracellular_popultaion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'extracellular', ['Popultaion'])

        # Adding M2M table for field units on 'Popultaion'
        m2m_table_name = db.shorten_name(u'extracellular_popultaion_units')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('popultaion', models.ForeignKey(orm[u'extracellular.popultaion'], null=False)),
            ('extendedunit', models.ForeignKey(orm[u'extracellular.extendedunit'], null=False))
        ))
        db.create_unique(m2m_table_name, ['popultaion_id', 'extendedunit_id'])


    def backwards(self, orm):
        # Deleting model 'CoordinateSystem'
        db.delete_table(u'extracellular_coordinatesystem')

        # Deleting model 'Penetration'
        db.delete_table(u'extracellular_penetration')

        # Deleting model 'Location'
        db.delete_table(u'extracellular_location')

        # Removing M2M table for field blocks on 'Location'
        db.delete_table(db.shorten_name(u'extracellular_location_blocks'))

        # Deleting model 'ExtendedUnit'
        db.delete_table(u'extracellular_extendedunit')

        # Deleting model 'Popultaion'
        db.delete_table(u'extracellular_popultaion')

        # Removing M2M table for field units on 'Popultaion'
        db.delete_table(db.shorten_name(u'extracellular_popultaion_units'))


    models = {
        u'broab.block': {
            'Meta': {'ordering': "['-rec_datetime', '-file_datetime', 'index']", 'object_name': 'Block'},
            'annotations': ('djorm_hstore.fields.DictionaryField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'file_origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'rec_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'broab.recordingchannel': {
            'Meta': {'object_name': 'RecordingChannel'},
            'annotations': ('djorm_hstore.fields.DictionaryField', [], {'blank': 'True'}),
            'coord_units': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file_origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'x_coord': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_coord': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z_coord': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'broab.recordingchannelgroup': {
            'Meta': {'object_name': 'RecordingChannelGroup'},
            'annotations': ('djorm_hstore.fields.DictionaryField', [], {'blank': 'True'}),
            'block': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'recording_channel_groups'", 'null': 'True', 'to': u"orm['broab.Block']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file_origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'recording_channels': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'recording_channel_groups'", 'symmetrical': 'False', 'to': u"orm['broab.RecordingChannel']"})
        },
        u'broab.unit': {
            'Meta': {'object_name': 'Unit'},
            'annotations': ('djorm_hstore.fields.DictionaryField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file_origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'recording_channel_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['broab.RecordingChannelGroup']", 'null': 'True', 'blank': 'True'})
        },
        u'electrode.electrode': {
            'Meta': {'object_name': 'Electrode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'uses': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'extracellular.coordinatesystem': {
            'Meta': {'object_name': 'CoordinateSystem'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'extracellular.extendedunit': {
            'Meta': {'object_name': 'ExtendedUnit', '_ormbases': [u'broab.Unit']},
            'multi': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'quality': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'quality_method': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'unit_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['broab.Unit']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'extracellular.location': {
            'Meta': {'object_name': 'Location'},
            'annotations': ('djorm_hstore.fields.DictionaryField', [], {'blank': 'True'}),
            'blocks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['broab.Block']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file_origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'penetration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['extracellular.Penetration']"})
        },
        u'extracellular.penetration': {
            'Meta': {'object_name': 'Penetration'},
            'alpha_angle': ('django.db.models.fields.FloatField', [], {'default': '90'}),
            'annotations': ('djorm_hstore.fields.DictionaryField', [], {'blank': 'True'}),
            'beta_angle': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'depth_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'electrode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['electrode.Electrode']"}),
            'file_origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'hemisphere': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lateral': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'rostral': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'rotation_angle': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['husbandry.Subject']"})
        },
        u'extracellular.popultaion': {
            'Meta': {'object_name': 'Popultaion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'units': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['extracellular.ExtendedUnit']", 'symmetrical': 'False'})
        },
        u'husbandry.subject': {
            'Meta': {'object_name': 'Subject'},
            'desciption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'})
        }
    }

    complete_apps = ['extracellular']