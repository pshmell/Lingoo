from django.conf.urls.defaults import patterns, include, url
from word.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$',
        upload_page),
    (r'^upload',
        upload_page),
    (r'^save',
        save),
    (r'^cloud/([^\s]+)/$',
        cloud_page),
    # todo handle files with spaces, etc in filename
    (r'^analysis/([^\s]+)/$',
        analysis_page),
    (r'^text',
        text_page),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/paul/Documents/Lingoo/media/'}),


    # append to analysis page: /([^\s]+)/$ ([^a-zA-Z0-9_\s-]+)
    # Examples:
    # url(r'^$', 'wc.views.home', name='home'),
    # url(r'^wc/', include('wc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
