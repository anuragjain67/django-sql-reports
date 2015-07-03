from django.conf.urls import url
from sqlreports.views import ReportList, ReportView, ReportSchema

urlpatterns = [
    url(r'sqlreports/$',
        ReportList.as_view(),
        name='sqlreports-report_list'
        ),
    url(r'sqlreports/(?P<report_id>\d+)/$',
        ReportView.as_view(), name='sqlreports-get_report'),

    url(r'sqlreports/schema/$',
        ReportSchema.as_view(), name='sqlreports-schema'),
]
