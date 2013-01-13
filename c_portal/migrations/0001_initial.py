# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table('c_portal_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16, db_index=True)),
        ))
        db.send_create_signal('c_portal', ['Tag'])

        # Adding model 'Member'
        db.create_table('c_portal_member', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, db_index=True)),
            ('aboutme', self.gf('django.db.models.fields.CharField')(max_length=4096)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('c_portal', ['Member'])

        # Adding M2M table for field tags on 'Member'
        db.create_table('c_portal_member_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('member', models.ForeignKey(orm['c_portal.member'], null=False)),
            ('tag', models.ForeignKey(orm['c_portal.tag'], null=False))
        ))
        db.create_unique('c_portal_member_tags', ['member_id', 'tag_id'])

        # Adding model 'Project'
        db.create_table('c_portal_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, db_index=True)),
            ('abstract', self.gf('django.db.models.fields.CharField')(default='', max_length=4096)),
        ))
        db.send_create_signal('c_portal', ['Project'])

        # Adding M2M table for field members on 'Project'
        db.create_table('c_portal_project_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['c_portal.project'], null=False)),
            ('member', models.ForeignKey(orm['c_portal.member'], null=False))
        ))
        db.create_unique('c_portal_project_members', ['project_id', 'member_id'])

        # Adding M2M table for field tags on 'Project'
        db.create_table('c_portal_project_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['c_portal.project'], null=False)),
            ('tag', models.ForeignKey(orm['c_portal.tag'], null=False))
        ))
        db.create_unique('c_portal_project_tags', ['project_id', 'tag_id'])

        # Adding model 'Article'
        db.create_table('c_portal_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['c_portal.Member'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['c_portal.Project'], null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 2, 0, 0), auto_now_add=True, blank=True)),
            ('mod_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 2, 0, 0), auto_now=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('abstract', self.gf('django.db.models.fields.CharField')(max_length=4096, null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(max_length=65536)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('c_portal', ['Article'])

        # Adding M2M table for field tags on 'Article'
        db.create_table('c_portal_article_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['c_portal.article'], null=False)),
            ('tag', models.ForeignKey(orm['c_portal.tag'], null=False))
        ))
        db.create_unique('c_portal_article_tags', ['article_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('c_portal_tag')

        # Deleting model 'Member'
        db.delete_table('c_portal_member')

        # Removing M2M table for field tags on 'Member'
        db.delete_table('c_portal_member_tags')

        # Deleting model 'Project'
        db.delete_table('c_portal_project')

        # Removing M2M table for field members on 'Project'
        db.delete_table('c_portal_project_members')

        # Removing M2M table for field tags on 'Project'
        db.delete_table('c_portal_project_tags')

        # Deleting model 'Article'
        db.delete_table('c_portal_article')

        # Removing M2M table for field tags on 'Article'
        db.delete_table('c_portal_article_tags')


    models = {
        'c_portal.article': {
            'Meta': {'object_name': 'Article'},
            'abstract': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['c_portal.Member']"}),
            'body': ('django.db.models.fields.TextField', [], {'max_length': '65536'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 2, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['c_portal.Project']", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
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