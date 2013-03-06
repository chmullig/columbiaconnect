from django.conf.urls import *
from views import *
from models import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'columbiaconnect.views.home', name='home'),
    # url(r'^columbiaconnect/', include('columbiaconnect.foo.urls')),
    url(r'^home/', home),
    url(r'^login/', login_page),
    url(r'^logout/', logout_page),
    url(r'^signup/', signup_page),
    url(r'^query/', query_page),
    url(r'^create_group/', create_groups_page),
    url(r'^create_group_call/', create_group),
    url(r'^$', home),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    url(r'^users/.+', users),
    url(r'^usergroup/.+', details),
    url(r'^groupimage/.+', groupimage),
    url(r'^join_group/.+', join_group),
)

urlpatterns += staticfiles_urlpatterns()
