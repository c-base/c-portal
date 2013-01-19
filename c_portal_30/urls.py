from django.conf.urls import patterns, include, url
from jsonrpc import jsonrpc_site
import api.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	url(r'comments/', include('django.contrib.comments.urls')),

    url(r'^wonderland/', include(admin.site.urls)),

	url(r'^rpc/', jsonrpc_site.dispatch),

	url(r'^account/', include('account.urls')),

	url(r'^polls/', include('polls.urls')),

	url(r'^shoutbox/', include('shoutbox.urls')),

	url(r'^getting-started/$', 'c_portal.views.getting_started'),

	url(r'^$', 'c_portal.views.portal_area'),

	url(
		r'^members/(?P<nickname>.*)/tag/(?P<tag_name>.*)/$',
		'c_portal.views.tag_member',
		),
	url(
		r'^members/(?P<nickname>.*)/untag/(?P<tag_name>.*)/$',
		'c_portal.views.untag_member',
		),
	url(
		r'^members/.*/join_project/$',
		'c_portal.views.join_project',
		),
	url(
		r'^members/(?P<nickname>.*)/add_tags/$',
		'c_portal.views.tag_member',
		),
	url(r'^members/.*/aboutme/$',
		'c_portal.views.change_aboutme',
		),
	url(r'^members/(?P<nickname>.*)/$', 'c_portal.views.member_area'),
	url(r'^members/$', 'c_portal.views.members'),


	url(
		r'^projects/(?P<project_name>.*)/tag/(?P<tag_name>.*)/$',
		'c_portal.views.tag_project',
		),
	url(
		r'^projects/(?P<project_name>.*)/untag/(?P<tag_name>.*)/$',
		'c_portal.views.untag_project',
		),
	url(
		r'^projects/(?P<project_name>.*)/add_tags/$',
		'c_portal.views.tag_project',
		),
	url(
		r'^projects/(?P<project_name>.*)/abstract/$',
		'c_portal.views.change_abstract',
		),
	url(r'^projects/(?P<project_name>.*)/join/$', 'c_portal.views.join_project'),
	url(r'^projects/(?P<project_name>.*)/leave/$', 'c_portal.views.leave_project'),
	url(r'^projects/(?P<project_name>.*)/$', 'c_portal.views.project_area'),
	url(r'^projects/$', 'c_portal.views.list_projects'),

	url(r'^tags/(?P<tag_name>.*)/', 'c_portal.views.tag'),

	url(r'^article/create/', 'c_portal.views.create_article'),
	url(
		r'^articles/(?P<article_id>\d+)/tag/(?P<tag_name>.*)/$',
		'c_portal.views.tag_article',
		),
	url(
		r'^articles/(?P<article_id>\d+)/untag/(?P<tag_name>.*)/$',
		'c_portal.views.untag_article',
		),
	url(
		r'^articles/(?P<article_id>\d+)/add_tags/$',
		'c_portal.views.tag_article',
		),
	url(r'^articles/(?P<article_id>\d+)/publish/$', 'c_portal.views.publish'),
	url(r'^articles/(?P<article_id>\d+)/unpublish/$', 'c_portal.views.unpublish'),
	url(r'^articles/(?P<pk>\d+)/edit/$', 'c_portal.views.edit_article'),
	url(r'^articles/(?P<pk>\d+)/delete/$', 'c_portal.views.delete_article'),
	url(r'^articles/(?P<pk>\d+)/$', 'c_portal.views.article'),
)

