Reports
=====
Write SQL, it will generate the report.


Quick start
-----------

1. Add "reports" to your INSTALLED_APPS setting like this::

        INSTALLED_APPS = (
                ...
                'sqlreports',
            )

2. Include the polls URLconf in your project urls.py like this::

    url(r'^reporting-service/', include('sqlreports.urls')),

3. Run `python manage.py migrate` to create the reports models.

Run Test APP
-----------
1. git clone https://github.com/anuragjain67/django-sql-reports.git
2. python setup.py develop
3. python test_app/manage.py migrate
4. python test_app/manage.py loaddata test_app/fixtures/data.json
5. python test_app/manage.py test
6. python test_app/manage.py runserver

For superuser
username = anurag
password = anurag

Todo:
-----------
1. Use only read connection:
       Right now it assumes that only super user run the reports.
       But later on we will only have read only connection.
2. Add the pagination feature.
3. Add hooks:
        1. Filter out the reports. 
        2. Own format out. Add example for JSON format output.
4. Add more test cases and add travis. 
5. Add proper docs with screenshots.
6. Add south support for migration purpose.
7. Reporting Chart.
8. Add the celery features to execute report in backend and add send email feature.
9. Add this DockerFile for faster demo. 
10. Add Playground feature for testing reports.


Courtesy:
-----------
1. Added schema view feature from [django-sql-explorer](https://github.com/epantry/django-sql-explorer)
2. Took idea of Report Generator and Report Formatter from [django-oscar](https://django-oscar.readthedocs.org)

