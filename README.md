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
    > username = anurag, password = anurag

Security:
-----------
Its recommended to use only readonly connection for this app.
Specify SQLREPORTS_CONNECTION_NAME in your settings.

Todo:
-----------
### Code Related:
1. Add the pagination feature.
2. Add Run in background feature.
3. Add more test cases
4. Add proper docs with screenshots.
5. Reporting Chart.
6. Add Playground feature for testing reports.

### Devops Related
1. Add travis. 
2. Dockerfile.
3. Add it to heroku.

Contributions:
-----------
* **Your contributions always welcome**
* Pick any code related todo and Give pull request
* You can bring ideas as well.

Courtesy:
-----------
1. Added schema view feature from [django-sql-explorer](https://github.com/epantry/django-sql-explorer)
2. Took idea of Report Generator and Report Formatter from [django-oscar](https://django-oscar.readthedocs.org)

