from django.conf.urls import patterns, url
from sqlreports.views import reports, report

urlpatterns = patterns('',
    url(r'sqlreports/$', reports, name='report_list'),
    url(r'sqlreports/(?P<report_id>\d+)/$', report, name='get_report')
)
