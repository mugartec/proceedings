from django.conf.urls import patterns, include, url
from django.contrib import admin
from papers.settings import MEDIA_ROOT, DEBUG
from publications.views import home, conference_instance

urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
    url(r'^conference_instance/(\d+)$', conference_instance, name='conference_instance'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
)

if DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$',
                             'django.views.static.serve',
                             {'document_root': MEDIA_ROOT}))
