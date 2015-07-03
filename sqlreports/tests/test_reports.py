from django.test import TestCase
from django.core.urlresolvers import reverse

from sqlreports.models import SQLReport, SQLReportParam

FIXTURES = ['data.json']


class BaseTestCase(TestCase):
    def login(self, username, password):
        '''
        Login method which logs in django test client
        '''
        self.client.login(username=username, password=password)


class TestReports(BaseTestCase):
    '''
    Test cases for Reports
    '''
    fixtures = FIXTURES

    def setUp(self):
        '''
        Initial setup of Test cases
        '''
        super(TestReports, self).setUp()
        self.login(username="anurag", password="anurag")

    def load_report(self):
        """ Hardcode sql for auth user"""
        r = SQLReport(name="GENERAL",
                      query="SELECT id, username from auth_user where id='{{USER_ID}}'")
        r.save()
        rp = SQLReportParam(report=r, param_key="USER_ID")
        rp.save()
        return r

    def test_report_api(self):
        '''test case for basic sqlreports'''
        report_obj = self.load_report()
        data = {"USER_ID": 1, "is_html": "yes"}
        response = self.client.get(
                        reverse('sqlreports-get_report',
                                kwargs={'report_id': report_obj.id}),
                        data=data
                    )
        self.assertIn("id", response.context["headers"])
        self.assertIn("username", response.context["headers"])
        self.assertEqual([{"id":1, "username":"anurag"}],
                         response.context["report_data"])
