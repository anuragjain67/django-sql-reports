import csv
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied


def download_csv_python_obj(headers, data_objs, file_name="sqlreports.csv"):
    """For given python objects it will return the csv file"""
    response = HttpResponse(mimetype='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=%s' % file_name
    # the csv writer
    writer = csv.writer(response)
    field_names = [header for header in headers]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for data_obj in data_objs:
        writer.writerow([data_obj[field] for field in field_names])
    return response

download_csv_python_obj.short_description = "Download selected as csv"


def validate_report_access(user, report):
    '''Validates if running a sqlreports is allowed or not'''
    # TODO: Instead of this provide hook.

    if user.is_superuser:
        # Super users are allowed everything
        return True

    if not user.is_staff:
        # Non Staff are never allowed access to sqlreports
        raise PermissionDenied("SQLReport access is not allowed.")

    # Allowed only if sqlreports is designated as a non-super user allowed
    if not report.user_allowed:
        raise PermissionDenied("SQLReport access is not allowed.")

    return True
