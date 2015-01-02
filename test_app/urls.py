from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',
    url(r'^reporting-service/', include('sqlreports.urls')),
    # Django Admin URL
    url(r'^admin/', include(admin.site.urls)),
)
