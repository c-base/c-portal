from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^login/$', 'account.views.auth_login'),
	url(r'^logout/$', 'account.views.auth_logout'),
	url(r'^c-profile/$', 'account.views.c_profile'),
)

