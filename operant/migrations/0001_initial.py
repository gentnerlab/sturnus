# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProtocolType'
        db.create_table(u'operant_protocoltype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'operant', ['ProtocolType'])

        # Adding model 'Protocol'
        db.create_table(u'operant_protocol', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('file_origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('annotations', self.gf('djorm_hstore.fields.DictionaryField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['operant.ProtocolType'], null=True, blank=True)),
        ))
        db.send_create_signal(u'operant', ['Protocol'])

        # Adding model 'TrialSet'
        db.create_table(u'operant_trialset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('file_origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('annotations', self.gf('djorm_hstore.fields.DictionaryField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('protocol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['operant.Protocol'], null=True, blank=True)),
        ))
        db.send_create_signal(u'operant', ['TrialSet'])

        # Adding model 'TrialType'
        db.create_table(u'operant_trialtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'operant', ['TrialType'])

        # Adding model 'TrialClass'
        db.create_table(u'operant_trialclass', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'operant', ['TrialClass'])

        # Adding model 'Trial'
        db.create_table(u'operant_trial', (
            (u'event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['broab.Event'], unique=True, primary_key=True)),
            ('index', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('tr_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['operant.TrialType'], null=True)),
            ('tr_class', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trial_set_as_class', null=True, to=orm['operant.TrialClass'])),
            ('stimulus', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trial_set_as_response', null=True, to=orm['operant.TrialClass'])),
            ('reinforced', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('trial_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['operant.TrialSet'])),
        ))
        db.send_create_signal(u'operant', ['Trial'])


    def backwards(self, orm):
        # Deleting model 'ProtocolType'
        db.delete_table(u'operant_protocoltype')

        # Deleting model 'Protocol'
        db.delete_table(u'operant_protocol')

        # Deleting model 'TrialSet'
        db.delete_table(u'operant_trialset')

        # Deleting model 'TrialType'
        db.delete_table(u'operant_trialtype')

        # Deleting model 'TrialClass'
        db.delete_table(u'operant_trialclass')

        # Deleting model 'Trial'
        db.delete_table(u'operant_trial')


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
        u'broab.event': {
            'Meta': {'object_name': 'Event'},
            'annotations': ('djorm_hstore.fields.DictionaryField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'duration': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'file_origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['broab.EventLabel']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': u"orm['broab.Segment']"}),
            'time': ('django.db.models.fields.FloatField', [], {})
        },
        u'broab.eventlabel': {
            'Meta': {'ordering': "['name']", 'object_name': 'EventLabel'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'broab.segment': {
            'Meta': {'ordering': "['-rec_datetime', '-file_datetime', 'index']", 'object_name': 'Segment'},
            'annotations': ('djorm_hstore.fields.DictionaryField', [], {'blank': 'True'}),
            'block': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'segments'", 'null': 'True', 'to': u"orm['broab.Block']"}),
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
        u'operant.protocol': {
            'Meta': {'object_name': 'Protocol'},
            'annotations': ('djorm_hstore.fields.DictionaryField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file_origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operant.ProtocolType']", 'null': 'True', 'blank': 'True'})
        },
        u'operant.protocoltype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ProtocolType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'operant.trial': {
            'Meta': {'object_name': 'Trial', '_ormbases': [u'broab.Event']},
            u'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['broab.Event']", 'unique': 'True', 'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'reinforced': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trial_set_as_response'", 'null': 'True', 'to': u"orm['operant.TrialClass']"}),
            'stimulus': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tr_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trial_set_as_class'", 'null': 'True', 'to': u"orm['operant.TrialClass']"}),
            'tr_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operant.TrialType']", 'null': 'True'}),
            'trial_set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operant.TrialSet']"})
        },
        u'operant.trialclass': {
            'Meta': {'ordering': "['name']", 'object_name': 'TrialClass'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'operant.trialset': {
            'Meta': {'object_name': 'TrialSet'},
            'annotations': ('djorm_hstore.fields.DictionaryField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file_origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'protocol': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operant.Protocol']", 'null': 'True', 'blank': 'True'})
        },
        u'operant.trialtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'TrialType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['operant']