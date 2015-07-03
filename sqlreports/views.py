from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.decorators import method_decorator
from django.http.response import HttpResponseForbidden
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from sqlreports.models import SQLReportParam, SQLReport
from sqlreports.core import ReportGenerator
from sqlreports.utils import schema_info


class ReportList(ListView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        filters = {}
        if not request.user.is_superuser:
            filters['user_allowed'] = True
        return render_to_response(
                    'sqlreports/sqlreports.html',
                    {
                     "sqlreports": SQLReport.objects.filter(
                                        **filters
                                        ).order_by('name')
                    }, RequestContext(request)
                )


class ReportView(DetailView):

    def _get_generator(self, is_html):
        formatter = 'HTML' if is_html else 'CSV'
        return ReportGenerator(formatter=formatter)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        report_id = kwargs.get('report_id')
        is_html = request.GET.get('is_html', False)
        is_csv = request.GET.get('is_csv', False)

        report = SQLReport.objects.get(pk=report_id)

        generator = self._get_generator(is_html)

        if not generator.is_available_to(request.user, report):
            return HttpResponseForbidden(
                    "You do not have access to"
                    " this report")

        param_dict, params = self._get_param_dict(request, report_id)

        context_to_send = {
                           'report': report,
                           'params': params,
                           'is_html': is_html,
                           'param_dict': param_dict
                           }
        if is_html or is_csv:
            try:
                report_data = generator.generate(report_id, param_dict)
                if not is_html:
                    return report_data
                context_to_send.update({
                                        'report_data': report_data,
                                        'headers': report_data[0].keys()
                                        })
            except IndexError:
                error_msg = "No data available for this sqlreports"
                context_to_send.update({'error_msg': error_msg})

        return render_to_response(
                'sqlreports/sqlreport.html',
                context_to_send, RequestContext(request)
                )

    def _get_param_dict(self, request, report_id):
        param_dict = {}
        params = SQLReportParam.objects.filter(report_id=report_id)
        for param in params:
            param_key = request.GET.get(param.param_key)
            if param_key:
                param_dict.update({param.param_key: param_key})
        return (param_dict, params)


class ReportSchema(DetailView):
    @method_decorator(login_required)
    def get(self, request):
        return render_to_response(
                    'sqlreports/schema.html',
                    {'schema': schema_info()}
                )
