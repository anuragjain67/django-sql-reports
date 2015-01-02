=====
Reports
=====
Write SQL, it will generate the report.


Quick start
-----------

1. Add "reports" to your INSTALLED_APPS setting like this::

```
INSTALLED_APPS = (
        ...
        'sqlreports',
    )
```

2. Include the polls URLconf in your project urls.py like this::

    url(r'^reporting-service/', include('sqlreports.urls')),


3. Run `python manage.py migrate` to create the reports models.


Todo:
1. Use only read connection:

       Right now it assumes that only super user run the reports.
       But later on we will only have read only connection.

2. Add the pagination feature.
3. Add hooks to filter out reports.
4. Add test cases and add it to travis.yml build
5. Add docker to make this application easier to get up and running
6. Add proper docs with screenshots.
7. Add south support for migration purpose.


