from django.db import models
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse


class SQLReport(models.Model):
    """
    It will contains sqlreports sql query
    """
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    query = models.TextField()
    user_allowed = models.BooleanField(
                        default=False,
                        help_text="Set to true to allow any user. Risky!"
                    )

    def __unicode__(self):
        return self.name

    def go_to_report(self):
        url = reverse('sqlreports-get_report', kwargs={"report_id": self.id})
        return mark_safe('<a href={url}>Go To SQLReport</a>'.format(url=url))

    class Meta:
        app_label = 'sqlreports'


class SQLReportParam(models.Model):
    """
    It will contains sqlreports sql query with params
    """
    report = models.ForeignKey(SQLReport)
    param_key = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128, default='', blank=True)
    help_text = models.CharField(max_length=512, default='', blank=True)
    choices = models.CharField(
                    max_length=2045,
                    help_text='Comma separated choices',
                    default='',
                    blank=True
                )

    @property
    def choice_list(self):
        return [x.strip() for x in self.choices.split(',')]

    class Meta:
        app_label = 'sqlreports'
