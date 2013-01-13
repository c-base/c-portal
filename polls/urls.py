from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(
            r'^(?P<poll_id>\d+)/$',
            'polls.views.poll_view',
            ),
        url(
            r'(?P<poll_id>\d+)/vote/',
            'polls.views.vote',
            ),
)

