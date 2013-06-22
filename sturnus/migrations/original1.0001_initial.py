# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subject'
        db.create_table('sturnus_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sex', self.gf('django.db.models.fields.CharField')(default='?', max_length=1)),
        ))
        db.send_create_signal('sturnus', ['Subject'])


    def backwards(self, orm):
        # Deleting model 'Subject'
        db.delete_table('sturnus_subject')


    models = {
        'sturnus.subject': {
            'Meta': {'object_name': 'Subject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '1'})
        }
    }

    complete_apps = ['sturnus']