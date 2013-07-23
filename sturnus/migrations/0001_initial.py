# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subject'
        db.create_table(u'sturnus_subject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('sex', self.gf('django.db.models.fields.CharField')(default='U', max_length=1)),
        ))
        db.send_create_signal(u'sturnus', ['Subject'])

        # Adding model 'Penetration'
        db.create_table(u'sturnus_penetration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hemisphere', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('rostral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lateral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('alpha_angle', self.gf('django.db.models.fields.FloatField')(default=90)),
            ('beta_angle', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('rotation_angle', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('depth_max', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'sturnus', ['Penetration'])


    def backwards(self, orm):
        # Deleting model 'Subject'
        db.delete_table(u'sturnus_subject')

        # Deleting model 'Penetration'
        db.delete_table(u'sturnus_penetration')


    models = {
        u'sturnus.penetration': {
            'Meta': {'object_name': 'Penetration'},
            'alpha_angle': ('django.db.models.fields.FloatField', [], {'default': '90'}),
            'beta_angle': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'depth_max': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hemisphere': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lateral': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rostral': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rotation_angle': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'sturnus.subject': {
            'Meta': {'object_name': 'Subject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'})
        }
    }

    complete_apps = ['sturnus']