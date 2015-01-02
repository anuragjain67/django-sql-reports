from django.contrib import admin
from sqlreports.models import SQLReportParam, SQLReport


class ReportParamInlineAdmin(admin.TabularInline):
    model = SQLReportParam
    extra = 1


class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'go_to_report')
    inlines = [
        ReportParamInlineAdmin
    ]

admin.site.register(SQLReport, ReportAdmin)
