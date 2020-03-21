# -*- coding: utf-8 -*-

from django.db.models import Count, Min, Max
from rest_framework import viewsets
import django_filters

from accesslog.models import AccessLog, DaySummary, MonthSummary
from accesslog.serializers import (
    AccessLogSerializer,
    DaySerializer,
    MonthSerializer,
    SourceSerializer
)


class SourceViewSet(viewsets.ModelViewSet):
    queryset = AccessLog.objects.values('source').annotate(
        total=Count('source'), time_min=Min('time'), time_max=Max('time'))
    serializer_class = SourceSerializer
    ordering = ('source',)


class AccessLogViewSet(viewsets.ModelViewSet):
    queryset = AccessLog.objects.all()
    serializer_class = AccessLogSerializer
    filter_fields = ('status', 'source')
    ordering = ('-time', 'source', 'status')


class DayFilter(django_filters.FilterSet):
    day_from = django_filters.DateFilter(name='day', lookup_type='gte')
    day_to = django_filters.DateFilter(name='day', lookup_type='lte')

    class Meta:
        model = DaySummary
        fields = ['source', 'day_from', 'day_to']


class DayViewSet(viewsets.ModelViewSet):
    queryset = DaySummary.objects.all()
    serializer_class = DaySerializer
    filter_class = DayFilter
    ordering = ('-day', 'source')


class MonthViewSet(viewsets.ModelViewSet):
    queryset = MonthSummary.objects.all()
    serializer_class = MonthSerializer
    filter_fields = ('year', 'source')
    ordering = ('-month', 'source')

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
