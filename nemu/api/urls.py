__author__ = 'Mateusz'
from django.conf.urls import patterns, include, url
from views import *


project_urls = patterns('',
                        url(r'^$', ProjectList.as_view(), name='project-list'),
                        url(r'^/(?P<title>[0-9a-zA-Z_-]+)$', ProjectDetail.as_view(), name='project-detail'),
                        )

urlpatterns = patterns('',
                       url(r'^projects', include(project_urls)),
                       )
