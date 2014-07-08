__author__ = 'Mateusz'
from django.conf.urls import patterns, include, url
from views import *

user_urls = patterns('',
                     url(r'^/(?P<username>[0-9a-zA-Z_-]+)$', UserDetail.as_view(), name='user-detail'),
                     url(r'^$', UserList.as_view(), name='user-list')
                     )

project_urls = patterns('',
                        url(r'^$', ProjectList.as_view(), name='project-list'),
                        url(r'^/(?P<title>[0-9a-zA-Z_-]+)$', ProjectDetail.as_view(), name='project-detail'),
                        url(r'^/(?P<project_id>[0-9a-zA-Z_-]+)/(?P<chapter_id>[0-9a-zA-Z_-]+)$', AssignedDetail.as_view(), name='assigned-detail'),
                        )

urlpatterns = patterns('',
                       url(r'^users', include(user_urls)),
                       url(r'^projects', include(project_urls)),
                       )
