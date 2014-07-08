from django.conf.urls import patterns, include, url
from django.contrib import admin
from api import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nemu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls'), name='api'),
    url(r'^$', views.OnePageAppView.as_view(), name='home'),
    (r'^rest-auth/', include('rest_auth.urls')),

)
