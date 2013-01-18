from django.conf.urls import patterns, include, url

shoutbox_patterns = patterns('',
    url(r'^$', 'shoutbox.views.show'),
    url(r'^add/$', 'shoutbox.views.shout_add'),
    url(r'^delete/(?P<shout_id>\d+)/$', 'shoutbox.views.shout_delete'),
)

urlpatterns = patterns('',
    url(r'^$','shoutbox.views.list'),
    url(r'^(?P<box_id>\d+)/', include(shoutbox_patterns)),
)
