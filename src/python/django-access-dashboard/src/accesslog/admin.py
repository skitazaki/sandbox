# -*- coding: utf-8 -*-

from django.contrib import admin
from accesslog.models import (
    AccessLog,
    MinuteSummary,
    HourSummary,
    DaySummary,
    MonthSummary
)


class AccessLogAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['time', 'protocol', 'status', 'size']}),
        ('Request information', {'fields': ['path', 'query', 'method'],
                                 'classes': ['collapse']}),
        ('User information', {'fields': ['referer', 'ua', 'ident', 'user'],
                              'classes': ['collapse']}),
        ('Misc. information', {'fields': ['host', 'trailing', 'source'],
                               'classes': ['collapse']}),
    ]
    list_display = ('time', 'status', 'method', 'path', 'source')


class MinuteSummaryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['source', 'time', 'total', 'path_kind', 'referer_kind',
                       'ua_kind', 'host_kind']}),
        ('Request/Response information', {
            'fields': ['status', 'method', 'protocol', 'size_min', 'size_max',
                       'size_avg'],
            'classes': ['collapse']}),
    ]
    list_display = ('time', 'total', 'source')


class HourSummaryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['source', 'day', 'hour', 'total', 'path_kind',
                       'referer_kind', 'ua_kind', 'host_kind']}),
        ('Request/Response information', {
            'fields': ['status', 'method', 'protocol', 'size_min', 'size_max',
                       'size_avg'],
            'classes': ['collapse']}),
    ]
    list_display = ('day', 'hour', 'total', 'source')


class DaySummaryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['source', 'day', 'total', 'path_kind', 'referer_kind',
                       'ua_kind', 'host_kind']}),
        ('Request/Response information', {
            'fields': ['status', 'method', 'protocol', 'size_min', 'size_max',
                       'size_avg'],
            'classes': ['collapse']}),
    ]
    list_display = ('day', 'total', 'source')


class MonthSummaryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['source', 'year', 'month', 'total', 'path_kind',
                       'referer_kind', 'ua_kind', 'host_kind']}),
        ('Request/Response information', {
            'fields': ['status', 'method', 'protocol', 'size_min', 'size_max',
                       'size_avg'],
            'classes': ['collapse']}),
    ]
    list_display = ('year', 'month', 'total', 'source')


admin.site.register(AccessLog, AccessLogAdmin)
admin.site.register(MinuteSummary, MinuteSummaryAdmin)
admin.site.register(HourSummary, HourSummaryAdmin)
admin.site.register(DaySummary, DaySummaryAdmin)
admin.site.register(MonthSummary, MonthSummaryAdmin)

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
