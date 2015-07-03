from collections import OrderedDict

from django.http import HttpResponse
from django.db import connection
from django.template import Context, Template
from django.utils.html import escape

from sqlreports.utils import CSVWriter
from sqlreports.models import SQLReport


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        OrderedDict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


class ReportFormatter(object):
    def filename(self):
        return self.filename_template


class ReportCSVFormatter(ReportFormatter):
    filename_template = 'sqlreports.csv'

    def get_csv_writer(self, file_handle, **kwargs):
        return CSVWriter(open_file=file_handle, **kwargs)

    def generate_response(self, headers, objects, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s' \
            % self.filename(**kwargs)
        self.generate_csv(response, headers, objects)
        return response

    def generate_csv(self, response, headers, objects):
        writer = self.get_csv_writer(response)
        # Write a first row with header information
        writer.writerow(headers)
        # Write data rows
        for data_obj in objects:
            writer.writerow([data_obj[header] for header in headers])
        return response


class ReportHTMLFormatter(ReportFormatter):

    def generate_response(self, headers, objects, **kwargs):
        return objects


class ReportGenerator(object):
    formatters = {
        'CSV_formatter': ReportCSVFormatter,
        'HTML_formatter': ReportHTMLFormatter
        }

    def __init__(self, **kwargs):
        formatter_name = '%s_formatter' % kwargs['formatter']
        self.formatter = self.formatters[formatter_name]()

    def generate(self, report_id, params):
        records = self.get_report_data(report_id, params)
        headers = records[0].keys()
        return self.formatter.generate_response(headers, records)

    def get_report_query(self, report_id, params_dict):
        """ QueryExample:
        select id, checkin_time from auth_user where email = '{{EMAIL_ID}}'
        """
        # FIXME: Need to include MySQL Escape
        query = SQLReport.objects.get(id=report_id).query
        t = Template(query)
        # Escaping Params
        escaped_params = {}
        for item in params_dict.items():
            escaped_params[item[0]] = escape(item[1])
        c = Context(escaped_params)
        return t.render(c)

    def get_report_data(self, report_id, params):
        """ For given sqlreports id and params it return the sqlreports data"""
        # FIXME: Connection should have only read only permission
        query = self.get_report_query(report_id, params)
        cursor = connection.cursor()
        cursor.execute(query)
        return dictfetchall(cursor)

    def is_available_to(self, user, report):
        """
        Checks whether this report is available to this user
        """
        if user.is_superuser:
            # Super users are allowed everything
            return True

        if not user.is_staff:
            # Non Staff are never allowed access to sqlreports
            return False

        # Allowed only if sqlreports is designated as a non-super user allowed
        if not report.user_allowed:
            return False

        return True
