from c_portal.models import *
from c_portal.forms import *
from polls.models import *
from polls.utils import *

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required


def portal_area(request):
	members = Member.objects.active()
	projects = Project.objects.all()
	featured = Article.objects.published().filter(
			featured=True,
			).order_by('-pub_date')[:10]
	tags = sorted(Tag.objects.all(), key=lambda x: x.popularity, reverse=True)
	latest_projects = Project.objects.all().order_by('-pk')[:8]
	return render_to_response('portal/area.django', locals())

def member_area(request, nickname):
	members = Member.objects.active()
	projects = Project.objects.all()
	member = get_object_or_404(Member, nickname=nickname)
	if request.is_ajax():
		if request.user.is_authenticated:
			if member.nickname == request.user.username:
				aboutme = ""
				try:
					aboutme = request.GET['aboutme']
				except: pass
				member.aboutme = aboutme
				member.save()
				return HttpResponse()
	my_projects = member.project_set.all()
	my_articles = Article.objects.published().filter(
			author=member).order_by('-pub_date')
	my_featured = my_articles.filter(featured=True)
	my_tags = sorted(member.tags.all(),
			key=lambda x: x.popularity, reverse=True)

	if request.user.is_authenticated():
		my_unpublished = Article.objects.unpublished().filter(
				author=member).order_by('-pub_date')
		projects_form = SelectProjectForm()
		project_form = ProjectForm()
		addtag_form = AddTagForm()
		joinproject_form = JoinProjectForm()
		aboutme_form = AboutmeForm(instance=member)
		poll = Poll.objects.get(pk=1)
		has_voted = member.nickname in [
				u.username for u in poll.participants.all()]
		total_votes = sum([c.votes for c in poll.choice_set.all()])
		progressbars = []
		for choice in poll.choice_set.all():
			progressbars.append(ProgressBar(
				choice.choice, total_votes, choice.votes))
	return render_to_response(
			'member/area.django', RequestContext(request, locals()))

def project_area(request, project_name):
	members = Member.objects.active()
	projects = Project.objects.all()
	project = get_object_or_404(Project, name=project_name)
	my_members = project.members.all()
	my_articles = Article.objects.published().filter(
			project=project).order_by('-pub_date')
	my_tags = sorted(project.tags.all(), key=lambda x: x.popularity, reverse=True)
	is_project_member = request.user.username in [m.nickname for m in project.members.all()]
	abstract_form = AbstractForm(instance=project)
	return render_to_response('project/area.django', RequestContext(request, locals()))

def join_project(request, project_name=None):
	member = get_object_or_404(Member, nickname=request.user.username)
	if request.method == 'POST':
		form = JoinProjectForm(request.POST)
		if form.is_valid():
			project_name = form.cleaned_data['name']
	try:
		project, created = Project.objects.get_or_create(name=project_name)
		if created:
			project.save()
		project.members.add(member)
		project.save()
	except:
		return HttpResponseRedirect('/projects/')
	return HttpResponseRedirect('/projects/%s/' % project_name)

def leave_project(request, project_name):
	member = get_object_or_404(Member, nickname=request.user.username)
	project = get_object_or_404(Project, name=project_name)
	if member.nickname in [m.nickname for m in project.members.all()]:
		project.members.remove(member)
		project.save()
		if len(project.members.all()) == 0:
			for article in project.article_set.all():
				article.project = None
				article.save()
			project.delete()
			return HttpResponseRedirect('/projects/')
	return HttpResponseRedirect('/projects/%s/' % project_name )

def members(request):
	members = Member.objects.active()
	projects = Project.objects.all()
	return render_to_response("member/list.django", locals())

def projects(request):
	members = Member.objects.active()
	projects = Project.objects.all()
	return render_to_response("projects.django", locals())

def list_projects(request):
	members = Member.objects.active()
	projects = Project.objects.all().order_by('-id')
	if request.user.is_authenticated():
		member = Member.objects.get(nickname=request.user.username)
		if request.method == "POST":
			form = JoinProjectForm(request.POST)
			if form.is_valid():
				name = form.cleaned_data['name']
				project, created = Project.objects.get_or_create(name=name)
				if created:
					project.save()
				project.members.add(member)
				project.save()
				return HttpResponseRedirect('/projects/%s/' % name)
		my_projects = [p.name for p in member.project_set.all()]
		createproject_form = JoinProjectForm()
		createproject_form.fields['name'].widget.attrs['class'] = 'input-block-level'
	return render_to_response('project/list.django', RequestContext(request, locals()))

def article(request, pk):
	if request.is_ajax():
		if request.user.is_authenticated:
			member = Member.objects.get(nickname=request.user.username)
			article = Article.objects.get(pk=pk)
			if article.id in [a.id for a in Article.objects.published()]:
				if article.author.nickname == member.nickname:
					state = project_pk = None
					try:
						state = request.GET['state']
					except: pass
					try:
						project_pk = request.GET['project_pk']
					except: pass
					if state is not None:
						if state.lower() == "true":
							article.featured = True
							article.save()
						elif state.lower() == "false":
							article.featured = False
							article.save()
						return HttpResponse(article.featured)
					elif project_pk is not None:
						if project_pk == "":
							article.project = None
						else:
							project = get_object_or_404(Project, pk=project_pk)
							if project.name in [p.name for p in member.project_set.all()]:
								article.project = project
						article.save()
						return HttpResponse(article.project)
		return HttpResponse()
	elif request.method == "GET":
		members = Member.objects.active()
		projects = Project.objects.all()
		article = get_object_or_404(Article, pk=pk)
		if not article.published and not request.user.username == article.author.nickname:
			return HttpResponseRedirect('/')
		title = article.title
		my_tags = sorted(article.tags.all(), key=lambda x: x.popularity, reverse=True)
		my_projects = dict(((p.id, p.name) for p in article.author.project_set.all()))
		project_form = ArticleProjectsForm()
		project_form.fields['project'].widget.attrs['class'] = 'input-block-level'
		if article.featured == True:
			featured = 'active'
		else:
			featured = ''
		return render_to_response('article/view.django', RequestContext(request, locals()))

def tag(request, tag_name):
	members = Member.objects.active()
	projects = Project.objects.all()
	tag = get_object_or_404(Tag, name=tag_name)
	my_members = tag.member_set.all().filter(active=True).select_related(
			).order_by('nickname')
	my_projects = tag.project_set.all().select_related().order_by('-id')
	my_articles = tag.article_set.all().filter(published=True).select_related(
			).order_by('-id')
	return render_to_response('tag/view.django', locals())

@login_required
def create_article(request):
	members = Member.objects.active()
	projects = Project.objects.all()
	if request.method == 'POST':
		member = get_object_or_404(Member, nickname=request.user.username)
		article = Article(author=member)
		form = ArticleForm(request.POST, instance=article)
		if form.is_valid():
			print 'valid'
			article.title = form.cleaned_data['title']
			article.abstract = form.cleaned_data['abstract']
			article.body = form.cleaned_data['body']
			article.save()
			return HttpResponseRedirect('/members/%s/' % member.nickname )
		else:
			form = ArticleForm(request.POST)
	else:
		form = ArticleForm()
	form.fields['title'].widget.attrs['class'] = 'input-block-level'
	form.fields['abstract'].widget.attrs['class'] = "input-block-level"
	form.fields['body'].widget.attrs['class'] = "input-block-level"
	return render_to_response(
			"article/create.django",
			RequestContext(request, locals())
			)

@login_required
def edit_article(request, pk):
	members = Member.objects.active()
	projects = Project.objects.all()
	member = Member.objects.get(nickname=request.user.username)
	article = get_object_or_404(Article, pk=pk)
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():
			if article.id in [a.id for a in member.article_set.all()]:
				article.title = form.cleaned_data['title']
				article.abstract = form.cleaned_data['abstract']
				article.body = form.cleaned_data['body']
				article.save()
				return HttpResponseRedirect('/articles/%s/' % pk)
	else:
		form = ArticleForm(instance=article)
		form.fields['title'].widget.attrs['class'] = 'input-block-level'
		form.fields['abstract'].widget.attrs['class'] = "input-block-level"
		form.fields['body'].widget.attrs['class'] = "input-block-level"
	return render_to_response("article/edit.django", RequestContext(request, locals()))

@login_required
def delete_article(request, pk):
	members = Member.objects.active()
	projects = Project.objects.all()
	member = Member.objects.get(nickname=request.user.username)
	article = get_object_or_404(Article, pk=pk)
	if article.id in [m.id for m in member.article_set.all()]:
		article.delete()
		return HttpResponseRedirect('/members/%s/' % request.user.username)
	return HttpResponse('we are excellent to eachother.')

@login_required
def tag_member(request, nickname, tag_name=None):
	member = Member.objects.get(nickname=nickname)
	if request.user.username == nickname:
		if request.method == 'POST':
			form = AddTagForm(request.POST)
			if form.is_valid():
				tags = form.cleaned_data['name']
				for tag_name in tags.split():
					if len(tag_name) > 24:
						tag_name = tag_name[:15]
					tag, created = Tag.objects.get_or_create(name=tag_name)
					if created:
						tag.save()
					member.tags.add(tag)
					member.save()
		else:
			tag, created = Tag.objects.get_or_create(name=tag_name)
			if created:
				tag.save()
			member.tags.add(tag)
			member.save()
	return HttpResponseRedirect('/members/%s/' % nickname)

@login_required
def untag_member(request, nickname, tag_name):
	member = Member.objects.get(nickname=nickname)
	if request.user.username == nickname:
		tag = get_object_or_404(Tag, name=tag_name)
		member.tags.remove(tag)
		if tag.is_empty:
			tag.delete()
	return HttpResponseRedirect('/members/%s/' % nickname)

@login_required
def tag_project(request, project_name, tag_name=None):
	project = Project.objects.get(name=project_name)
	if request.user.username in [m.nickname for m in project.members.all()]:
		if request.method == 'POST':
			form = AddTagForm(request.POST)
			if form.is_valid():
				tags = form.cleaned_data['name']
				for tag_name in tags.split():
					if len(tag_name) > 24:
						tag_name = tag_name[:15]
					tag, created = Tag.objects.get_or_create(name=tag_name)
					if created:
						tag.save()
					project.tags.add(tag)
					project.save()
		else:
			tag, created = Tag.objects.get_or_create(name=tag_name)
			if created:
				tag.save()
			project.tags.add(tag)
			project.save()
	return HttpResponseRedirect('/projects/%s/' % project_name)

@login_required
def untag_project(request, project_name, tag_name):
	project = Project.objects.get(name=project_name)
	if request.user.username in [m.nickname for m in project.members.all()]:
		tag = get_object_or_404(Tag, name=tag_name)
		project.tags.remove(tag)
		project.save()
		if tag.is_empty:
			tag.delete()
	return HttpResponseRedirect('/projects/%s/' % project_name)

@login_required
def tag_article(request, article_id, tag_name=None):
	article = Article.objects.get(pk=article_id)
	if request.user.username == article.author.nickname:
		if request.method == 'POST':
			form = AddTagForm(request.POST)
			if form.is_valid():
				tags = form.cleaned_data['name']
				for tag_name in tags.split():
					if len(tag_name) > 24:
						tag_name = tag_name[:15]
					tag, created = Tag.objects.get_or_create(name=tag_name)
					if created:
						tag.save()
					article.tags.add(tag)
					article.save()
		else:
			tag, created = Tag.objects.get_or_create(name=tag_name)
			if created:
				tag.save()
			article.tags.add(tag)
			article.save()
	return HttpResponseRedirect('/articles/%s/' % article_id)

@login_required
def untag_article(request, article_id, tag_name):
	article = Article.objects.get(pk=article_id)
	if request.user.username == article.author.nickname:
		tag = get_object_or_404(Tag, name=tag_name)
		article.tags.remove(tag)
		article.save()
		if tag.is_empty:
			tag.delete()
	return HttpResponseRedirect('/articles/%s/' % article_id)

@login_required
def change_aboutme(request):
	member = Member.objects.get(nickname=request.user.username)
	if request.method == 'POST':
		form = AboutmeForm(request.POST)
		if form.is_valid():
			aboutme = form.cleaned_data['aboutme']
			member.aboutme = aboutme
			member.save()
	return HttpResponseRedirect('/members/%s/' % member.nickname)

@login_required
def change_abstract(request, project_name):
	member = Member.objects.get(nickname=request.user.username)
	project = get_object_or_404(Project, name=project_name)
	if request.method == 'POST':
		form = AbstractForm(request.POST)
		if form.is_valid():
			abstract = form.cleaned_data['abstract']
			project.abstract = abstract
			project.save()
	return HttpResponseRedirect('/projects/%s/' % project.name)

@login_required
def publish(request, article_id):
	article = get_object_or_404(Article, pk=article_id)
	if request.user.username == article.author.nickname:
		article.published = True
		article.save()
	return HttpResponseRedirect('/members/%s/' % request.user.username)

@login_required
def unpublish(request, article_id):
	article = get_object_or_404(Article, pk=article_id)
	if request.user.username == article.author.nickname:
		article.published = False
		article.save()
	return HttpResponseRedirect('/members/%s/' % request.user.username)

def getting_started(request):
	gs = get_object_or_404(Article, title='getting-started')
	return article(request, pk=gs.pk)

