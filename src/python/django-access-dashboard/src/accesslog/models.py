# -*- coding: utf-8 -*-

from django.db import models
from jsonfield import JSONField


class AccessLog(models.Model):
    time = models.DateTimeField('access time')
    host = models.GenericIPAddressField()
    path = models.CharField(max_length=1000, null=True, blank=True)
    query = models.CharField(max_length=4000, null=True, blank=True)
    # TODO: Restrict values with "choices" argument.
    method = models.CharField(max_length=10)
    # TODO: Restrict values with "choices" argument.
    protocol = models.CharField(max_length=10)
    status = models.PositiveSmallIntegerField()
    size = models.PositiveIntegerField(null=True, blank=True)
    referer = models.CharField(max_length=200, null=True, blank=True)
    ua = models.CharField('User Agent', max_length=200, null=True, blank=True)
    ident = models.CharField(max_length=200, null=True, blank=True)
    user = models.CharField(max_length=200, null=True, blank=True)
    trailing = models.CharField(max_length=1000, null=True, blank=True)
    source = models.CharField(max_length=200, default='default')

    def __str__(self):
        return '{} {}'.format(self.time.strftime('%Y-%m-%d %H:%M:%S'),
                              self.path)


class StatisticsBase(models.Model):
    total = models.PositiveIntegerField()
    host_kind = models.PositiveIntegerField('Kind of hosts')
    path_kind = models.PositiveIntegerField('Kind of paths')
    protocol = JSONField()
    method = JSONField()
    status = JSONField()
    size_min = models.PositiveIntegerField('Minimum size', null=True)
    size_max = models.PositiveIntegerField('Maximum size', null=True)
    size_avg = models.FloatField('Average size', null=True)
    referer_kind = models.PositiveIntegerField('Kind of referers')
    ua_kind = models.PositiveIntegerField('Kind of user agents')

    class Meta:
        abstract = True


class MinuteSummary(StatisticsBase):
    source = models.CharField(max_length=200)
    time = models.DateTimeField()

    class Meta:
        unique_together = ('source', 'time')


class HourSummary(StatisticsBase):
    source = models.CharField(max_length=200)
    day = models.DateField()
    hour = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('source', 'day', 'hour')


class DaySummary(StatisticsBase):
    source = models.CharField(max_length=200)
    day = models.DateField()

    class Meta:
        unique_together = ('source', 'day')


class MonthSummary(StatisticsBase):
    source = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('source', 'year', 'month')

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
