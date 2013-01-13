# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Article.abstract'
        db.alter_column('c_portal_article', 'abstract', self.gf('django.db.models.fields.TextField')(max_length=4096, null=True))

    def backwards(self, orm):

        # Changing field 'Article.abstract'
        db.alter_column('c_portal_article', 'abstract', self.gf('django.db.models.fields.CharField')(max_length=4096, null=True))

    models = {
        'c_portal.article': {
            'Meta': {'object_name': 'Article'},
            'abstract': ('django.db.models.fields.TextField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['c_portal.Member']"}),
            'body': ('django.db.models.fields.TextField', [], {'max_length': '65536'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 5, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['c_portal.Project']", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 5, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['c_portal.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'})
        },
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16', 'db_index': 'True'})
        }
    }

    complete_apps = ['c_portal']