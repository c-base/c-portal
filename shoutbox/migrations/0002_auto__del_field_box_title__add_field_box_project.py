# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Box.title'
        db.delete_column('shoutbox_box', 'title')

        # Adding field 'Box.project'
        db.add_column('shoutbox_box', 'project',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['c_portal.Project'], unique=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Box.title'
        db.add_column('shoutbox_box', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=32),
                      keep_default=False)

        # Deleting field 'Box.project'
        db.delete_column('shoutbox_box', 'project_id')


    models = {
        'c_portal.member': {
            'Meta': {'object_name': 'Member'},
            'aboutme': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['c_portal.Tag']", 'null': 'True', 'blank': 'True'})
        },
        'c_portal.project': {
            'Meta': {'object_name': 'Project'},
            'abstract': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4096'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['c_portal.Member']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['c_portal.Tag']", 'null': 'True', 'blank': 'True'})
        },
        'c_portal.tag': {
            'Meta': {'object_name': 'Tag'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 15, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '24', 'db_index': 'True'})
        },
        'shoutbox.box': {
            'Meta': {'object_name': 'Box'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['c_portal.Project']", 'unique': 'True'})
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