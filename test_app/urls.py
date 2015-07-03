from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
               url(r'^reporting-service/', include('sqlreports.urls')),
               # Django Admin URL
               url(r'^admin/', include(admin.site.urls)),
               ]
