from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'search.views.index', name='home'),
    url(r'^direct_targets', 'search.views.direct_search',
        name='direct_search'),
    url(r'^enrichment_analysis', 'search.views.enrichment_analysis',
        name='enrichment_analysis'),
    url(r'^query_db', 'search.views.query_db', name='query_db'),
    url(r'^download/(?P<size>(all|page))',
        'search.views.download', name='download'),
    url(r'^download_file/(?P<fileid>\d+)',
        'search.views.download_file', name='download_file'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
