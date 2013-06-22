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
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('sex', self.gf('django.db.models.fields.CharField')(default='U', max_length=1)),
        ))
        db.send_create_signal('sturnus', ['Subject'])

        # Adding model 'Block'
        db.create_table('sturnus_block', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sturnus.Subject'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('sturnus', ['Block'])

        # Adding model 'Trial'
        db.create_table('sturnus_trial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sturnus.Block'])),
            ('tr_num', self.gf('django.db.models.fields.IntegerField')()),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('sturnus', ['Trial'])

        # Adding unique constraint on 'Trial', fields ['block', 'datetime']
        db.create_unique('sturnus_trial', ['block_id', 'datetime'])

        # Adding unique constraint on 'Trial', fields ['block', 'tr_num']
        db.create_unique('sturnus_trial', ['block_id', 'tr_num'])

        # Adding model 'BehaviorTrial'
        db.create_table('sturnus_behaviortrial', (
            ('trial_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sturnus.Trial'], unique=True, primary_key=True)),
            ('tr_type', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('tr_class', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('response', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('feed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timeout', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cum_correct', self.gf('django.db.models.fields.IntegerField')()),
            ('cum_correct_thresh', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('sturnus', ['BehaviorTrial'])


    def backwards(self, orm):
        # Removing unique constraint on 'Trial', fields ['block', 'tr_num']
        db.delete_unique('sturnus_trial', ['block_id', 'tr_num'])

        # Removing unique constraint on 'Trial', fields ['block', 'datetime']
        db.delete_unique('sturnus_trial', ['block_id', 'datetime'])

        # Deleting model 'Subject'
        db.delete_table('sturnus_subject')

        # Deleting model 'Block'
        db.delete_table('sturnus_block')

        # Deleting model 'Trial'
        db.delete_table('sturnus_trial')

        # Deleting model 'BehaviorTrial'
        db.delete_table('sturnus_behaviortrial')


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