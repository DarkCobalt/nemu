from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nemu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('auth.urls'), name='auth'),
    url(r'login/', 'auth.views.AuthLogin', name='login'),
    url(r'logout/', 'auth.views.AuthLogout', name='logout'),
    url(r'^$', 'workflow.views.index', name='home'),
)
