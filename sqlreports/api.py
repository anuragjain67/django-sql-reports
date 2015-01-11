import MySQLdb
from collections import OrderedDict

from django.db import connection, models
from django.template import Context, Template

from sqlreports.models import SQLReport
from sqlreports import app_settings


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        OrderedDict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def get_report_query(report_id, params):
    """ QueryExample:
    select id, checkin_time from auth_user where email = '{{EMAIL_ID}}'
    """
    # FIXME: Need to include MySQL Escape
    query = SQLReport.objects.get(id=report_id).query
    t = Template(query)

    # Escaping Params
    escaped_params = {}
    for item in params.items():
        escaped_params[item[0]] = MySQLdb.escape_string(item[1])
    c = Context(escaped_params)
    return t.render(c)


def get_report_data(report_id, params):
    """ For given sqlreports id and params it return the sqlreports data"""
    # FIXME: Connection should have only read only permission
    query = get_report_query(report_id, params)
    cursor = connection.cursor()
    cursor.execute(query)
    return dictfetchall(cursor)


def schema_info():
    """
    Construct schema information via introspection of the django models in the database.

    :return: Schema information of the following form, sorted by db_table_name.
        [
            ("package.name -> ModelClass", "db_table_name",
                [
                    ("db_column_name", "DjangoFieldType"),
                    (...),
                ]
            )
        ]

    """

    ret = []
    apps = [a for a in models.get_apps() if a.__package__ not in app_settings.EXCLUDE_APPS]
    for app in apps:
        for model in models.get_models(app):
            friendly_model = "%s -> %s" % (app.__package__, model._meta.object_name)
            ret.append((
                          friendly_model,
                          model._meta.db_table,
                          [_format_field(f) for f in model._meta.fields]
                      ))

            #Do the same thing for many_to_many fields. These don't show up in the field list of the model
            #because they are stored as separate "through" relations and have their own tables
            ret += [(
                       friendly_model,
                       m2m.rel.through._meta.db_table,
                       [_format_field(f) for f in m2m.rel.through._meta.fields]
                    ) for m2m in model._meta.many_to_many]
    
    return sorted(ret, key=lambda t: t[1])


def _format_field(field):
    return (field.get_attname_column()[1], field.get_internal_type())
