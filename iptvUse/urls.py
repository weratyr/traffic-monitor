from django.conf.urls import patterns, include, url

from traff import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^cuptureTraffic', views.cuptureTraffic, name='cuptureTraffic'),
    url(r'^createDummyDB', views.createDummyDB, name='createDummyDB'),
    # Examples:
    # url(r'^$', 'iptvUse.views.home', name='home'),
    # url(r'^iptvUse/', include('iptvUse.foo.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'traff/assets'}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
