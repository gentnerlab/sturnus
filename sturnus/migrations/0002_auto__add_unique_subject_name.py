# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Subject', fields ['name']
        db.create_unique('sturnus_subject', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Subject', fields ['name']
        db.delete_unique('sturnus_subject', ['name'])


    models = {
        'sturnus.subject': {
            'Meta': {'object_name': 'Subject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'X'", 'max_length': '1'})
        }
    }

    complete_apps = ['sturnus']