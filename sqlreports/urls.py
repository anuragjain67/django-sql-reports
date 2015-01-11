from django.conf.urls import patterns, url
from sqlreports.views import reports, report, schema

urlpatterns = patterns('',
    url(r'sqlreports/$', reports, name='report_list'),
    url(r'sqlreports/(?P<report_id>\d+)/$', report, name='get_report'),
    url(r'sqlreports/schema-info/$', schema, name='get_schema'),
)
