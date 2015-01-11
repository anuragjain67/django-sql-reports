from django.conf import settings

EXCLUDE_APPS = getattr(settings, 'EXCLUDE_APPS',
                       (
                        'django.contrib.contenttypes',
                        'django.contrib.sessions',
                        'django.contrib.admin'
                        )
                       )
