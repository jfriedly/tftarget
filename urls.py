from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'search.views.search', name='home'),
    url(r'^download/(?P<size>(all|page))',
        'search.views.download', name='download'),
    url(r'^download_file/(?P<fileid>\d+)',
        'search.views.download_file', name='download_file'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
