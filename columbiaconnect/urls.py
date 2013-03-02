from django.conf.urls import patterns, include, url
from columbiaconnect.views import home, current_datetime, hours_ahead
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'columbiaconnect.views.home', name='home'),
    # url(r'^columbiaconnect/', include('columbiaconnect.foo.urls')),
    url(r'^home/', home),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
