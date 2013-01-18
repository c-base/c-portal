from django.db import models

from django.utils import timezone as tz
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.core import serializers

from c_portal.managers import *

import datetime

import json


class Tag(models.Model):
	name = models.CharField(max_length=24, unique=True, db_index=True)
	create_date = models.DateTimeField(auto_now_add=True, default=tz.now())

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.lower()
		return super(Tag, self).save(*args, **kwargs)

	@property
	def is_empty(self):
		if len(self.member_set.all()) == 0:
			if len(self.project_set.all()) == 0:
				if len(self.article_set.all()) == 0:
					return True
		return False

	@property
	def popularity(self):
		members = len(self.member_set.all())
		projects = len(self.project_set.all())
		articles = len(self.article_set.all())
		return members + projects + articles

class Member(models.Model):
	nickname = models.CharField(max_length=64, unique=True, db_index=True)
	aboutme = models.CharField(max_length=4096)
	tags = models.ManyToManyField(Tag, blank=True, null=True)
	active = models.BooleanField(default=True)
	objects = MemberManager()

	def __unicode__(self):
		return self.nickname

	def get_profile(self):
		return User.objects.get(username=self.nickname)

	def get_active(self):
		return Member.objects.filter(active=True)

	def serialize(self):
		return {
				'model': 'c_portal.member',
				'pk': self.id,
				'fields': {
					'nickname': self.nickname,
					'aboutme': self.aboutme,
					'tags': [t.name for t in self.tags.all()],
					},
				}

class Project(models.Model):
	name = models.CharField(max_length=64, unique=True, db_index=True)
	abstract = models.CharField(max_length=4096, default='')
	members = models.ManyToManyField(Member)
	tags = models.ManyToManyField(Tag, blank=True, null=True)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		super(Project, self).save(*args, **kwargs)
		if self.name in [g.name for g in Group.objects.all()]:
			for member in self.members.all():
				user = User.objects.get(username=member.nickname)
				if not self.name in [g.name for g in user.groups.all()]:
					self.members.remove(member)
				super(Project, self).save(*args, **kwargs)
				if len(self.members.all()) == 0:
					self.delete()


class ContentNode(models.Model):
	title = models.CharField(max_length=64, db_index=True)
	author = models.ForeignKey(Member)
	project = models.ForeignKey(
			Project,
			null = True,
			blank = True
			)
	pub_date = models.DateTimeField(auto_now_add=True, default=tz.now())
	mod_date = models.DateTimeField(auto_now=True, default=tz.now())
	tags = models.ManyToManyField(Tag, blank=True, null=True)
	published = models.BooleanField(default=False)
	objects = ContentManager()

	class Meta:
		abstract = True

	def __unicode__(self):
		return self.title


class Article(ContentNode):
	abstract = models.TextField(max_length=4096, blank=True, null=True)
	body = models.TextField(max_length=65536)
	featured = models.BooleanField(default=False)
