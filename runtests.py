import os
import sys

from django.conf import settings

DIRNAME = os.path.dirname(__file__)
settings.configure(DEBUG=True,
                   DATABASES={
                              'default': {
                                          'ENGINE': 'django.db.backends.sqlite3',
                                          'NAME': os.path.join(DIRNAME, 'database.db')
                                          }
                              },
                   INSTALLED_APPS=('django.contrib.auth',
                                   'django.contrib.contenttypes',
                                   'django.contrib.sessions',
                                   'django.contrib.admin',
                                   'django.contrib.staticfiles',
                                   'sqlreports',
                                   'sqlreports.tests',),
                   ROOT_URLCONF='sqlreports.urls',
                   USE_TZ=True,
                   STATIC_URL = '/static/',
                   STATICFILES_DIRS = (os.path.join(DIRNAME, "static"))
                   )


from django.test.runner import DiscoverRunner

test_runner = DiscoverRunner(pattern='test*.py')
failures = test_runner.run_tests(['sqlreports'])
#failures = DjangoTestSuiteRunner(verbosity=1).run_tests(['sqlreports'])
if failures:
    sys.exit(failures)