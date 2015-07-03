from django.core.exceptions import ImproperlyConfigured
import csv
from django.db import models
from sqlreports import app_settings
from django.db.models.loading import get_apps, get_models


class CSVWriter(object):
    def __init__(self, filename=None, open_file=None):
        if filename is open_file is None:
            raise ImproperlyConfigured(
                "You need to specify either a filename or an open file")
        self.filename = filename
        self.f = open_file
        self.writer = None

    def writerow(self, row):
        if self.writer is None:
            self.writer = csv.writer(self.f)
        self.writer.writerow(list(row))

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


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
    apps = [a for a in get_apps() if a.__package__ not in app_settings.EXCLUDE_APPS]
    print apps
    for app in apps:
        for model in get_models(app):
            friendly_model = "%s -> %s" % (app.__package__, model._meta.object_name)
            ret.append((
                          friendly_model,
                          model._meta.db_table,
                          [_format_field(f) for f in model._meta.fields]
                      ))

            # Do the same thing for many_to_many fields.
            # These don't show up in the field list of the model
            # because they are stored as separate "through"
            # relations and have their own tables
            ret += [(
                       friendly_model,
                       m2m.rel.through._meta.db_table,
                       [_format_field(f) for f in m2m.rel.through._meta.fields]
                    ) for m2m in model._meta.many_to_many]
    return sorted(ret, key=lambda t: t[1])


def _format_field(field):
    return (field.get_attname_column()[1], field.get_internal_type())
