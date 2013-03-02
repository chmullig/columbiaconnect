from django.conf.urls import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()


from views import home

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'columbiaconnect.views.home', name='home'),
    # url(r'^columbiaconnect/', include('columbiaconnect.foo.urls')),
    url(r'^home/', home),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
)
