__author__ = 'Mateusz'
from django.conf.urls import patterns, url, include
from views import AuthView, UserView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api', UserView, 'list')

urlpatterns = patterns(
    '',
    url(r'^user/', include(router.urls)), #user details in JSON
    url(r'^$', AuthView.as_view(), name='authenticate'), #login + auth
)