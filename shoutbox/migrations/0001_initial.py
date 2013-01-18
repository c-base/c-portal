# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Box'
        db.create_table('shoutbox_box', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('shoutbox', ['Box'])

        # Adding model 'Shout'
        db.create_table('shoutbox_shout', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('box', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shoutbox.Box'])),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('shout', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('shoutbox', ['Shout'])


    def backwards(self, orm):
        # Deleting model 'Box'
        db.delete_table('shoutbox_box')

        # Deleting model 'Shout'
        db.delete_table('shoutbox_shout')


    models = {
        'shoutbox.box': {
            'Meta': {'object_name': 'Box'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'shoutbox.shout': {
            'Meta': {'object_name': 'Shout'},
            'box': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shoutbox.Box']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'shout': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['shoutbox']