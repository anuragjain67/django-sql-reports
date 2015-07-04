from django.conf import settings

SQLREPORTS_EXCLUDE_APPS = getattr(settings, 'SQLREPORTS_EXCLUDE_APPS',
                                  (
                                   'django.contrib.contenttypes',
                                   'django.contrib.sessions',
                                   'django.contrib.admin'
                                   )
                                  )

SQLREPORTS_CONNECTION_NAME = getattr(settings,
                                     'SQLREPORTS_CONNECTION_NAME',
                                     None)
