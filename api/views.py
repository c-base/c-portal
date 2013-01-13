# -*- coding: utf8 -*-

from c_portal.models import Tag, Member, Project, Article

from django.shortcuts import get_object_or_404
from django.core import serializers

from jsonrpc import jsonrpc_method

import json


def _get_params_from_json_request(request):
	return (
			# uh oh this looks so evil, but I have no better idea, so far
			json.loads(request.POST.dict().keys()[0])['params'][0],
			json.loads(request.POST.dict().keys()[0])['params'][1],
			)

@jsonrpc_method('api.get_member')
def get_member(request, nickname):
	member = Member.objects.get(nickname=nickname)
	return json.loads(
			serializers.serialize(
				'json',
				[ member ],
				)
			)

@jsonrpc_method('api.add_me', authenticated=True)
def add_me(request):
	nickname, password = _get_params_from_json_request(request)
	member, created = Member.objects.get_or_create(nickname=nickname)
	if created:
		member.save()
	return json.loads(
			serializers.serialize(
				'json',
				[ member ],
				)
			)

@jsonrpc_method('api.set_aboutme', authenticated=True)
def set_aboutme(request, aboutme):
	nickname, password = _get_params_from_json_request(request)
	member = Member.objects.get(nickname=nickname)
	member.aboutme = str(aboutme)
	member.save()
	return

@jsonrpc_method('api.join_project', authenticated=True)
def join_project(request, project_name, abstract=''):
	nickname, password = _get_params_from_json_request(request)
	member = Member.objects.get(nickname=nickname)
	project, created = Project.objects.get_or_create(name=project_name)
	if created:
		project.abstract = abstract
	project.members.add(member)
	project.save()
	return

@jsonrpc_method('api.leave_project', authenticated=True)
def leave_project(request, project_name):
	nickname, password = _get_params_from_json_request(request)
	member = Member.objects.get(nickname=nickname)
	project = Project.objects.get(name=project_name)
	project.members.remove(member)
	if len(project.members.all()) == 0:
		project.delete()
	else:
		project.save()
	return

@jsonrpc_method('api.get_my_projects', authenticated=True)
def get_my_projects(request):
	nickname, password = _get_params_from_json_request(request)
	member = Member.objects.get(nickname=nickname)
	return json.loads(
			serializers.serialize(
				'json',
				member.project_set.all(),
				)
			)

@jsonrpc_method('api.set_project_abstract', authenticated=True)
def set_project_abstract(request, project_name, abstract):
	project = Project.objects.get(name=project_name)
	project.abstract = abstract
	project.save()
	return

@jsonrpc_method('api.get_my_articles', authenticated=True)
def get_my_articles(request):
	nickname, password = _get_params_from_json_request(request)
	member = Member.objects.get(nickname=nickname)
	return json.loads(
			serializers.serialize(
				'json',
				Article.objects.published().filter(author=member),
				)
			)

@jsonrpc_method('api.add_article', authenticated=True)
def add_article(request, title, abstract=None, body=None, featured=False):
	nickname, password = _get_params_from_json_request(request)
	member = Member.objects.get(nickname=nickname)
	article = Article(
			title = title,
			abstract = abstract,
			body = body,
			featured = featured,
			)
	article.author = member
	article.save()
	return json.loads(
			serializers.serialize(
				'json',
				[ article ],
				)
			)

@jsonrpc_method('api.delete_article', authenticated=True)
def delete_article(request, pk):
	nickname, password = _get_params_from_json_request(request)
	member = Member.objects.get(nickname=nickname)
	member_articles = member.article_set.all()
	article = Article.objects.get(pk=pk)
	if article.pk in [ a.pk for a in member_articles ]:
		article.delete()

@jsonrpc_method('api.set_article', authenticated=True)
def set_article(request,
		pk,
		title=None,
		abstract=None,
		body=None,
		featured=None,
		project=None,
		):
	nickname, password = _get_params_from_json_request(request)
	member = Member.objects.get(nickname=nickname)
	member_articles = member.article_set.all()
	article = Article.objects.get(pk=pk)
	if article.pk in [ a.pk for a in member_articles ]:
		if title is not None:
			article.title = title
		if abstract is not None:
			article.abstract = abstract
		if body is not None:
			article.body = body
		if featured is not None:
			article.featured = featured
		if project is not None:
			p = Project.objects.get(name=project)
			article.project = p
		article.save()
		return json.loads(
				serializers.serialize(
					'json',
					[ article ],
					)
				)

@jsonrpc_method('api.list_members')
def list_members(request):
	return json.loads(
			serializers.serialize(
				'json',
				Member.objects.all(),
				)
			)

@jsonrpc_method('api.list_projects')
def list_projects(request):
	return json.loads(
			serializers.serialize(
				'json',
				Project.objects.all(),
				)
			)

@jsonrpc_method('api.list_articles')
def list_articles(request, member=None, project=None):
	if member is not None:
		output = Member.objects.get(nickname=member).article_set.all().order_by('-pub_date')
	elif project is not None:
		output = Project.objects.get().article_set.all().order_by('-pub_date')
	else:
		output = Article.objects.all().order_by('-pub_date')
	output = output.filter(featured=True)
	return json.loads(
			serializers.serialize(
				'json',
				output,
				)
			)


