# -*- coding: utf-8 -*-

from rest_framework import serializers

from accesslog.models import AccessLog, DaySummary, MonthSummary


class SourceSerializer(serializers.Serializer):
    source = serializers.CharField(max_length=200)
    total = serializers.IntegerField()
    time_min = serializers.DateTimeField()
    time_max = serializers.DateTimeField()


class AccessLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccessLog
        fields = ('id', 'time', 'host', 'path', 'query', 'method', 'protocol',
                  'status', 'size', 'referer', 'ua', 'trailing', 'source')


class DaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DaySummary
        fields = ('id', 'day', 'host_kind', 'path_kind', 'protocol', 'method',
                  'status', 'size_min', 'size_max', 'size_avg', 'referer_kind',
                  'ua_kind', 'total', 'source')


class MonthSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MonthSummary
        fields = ('id', 'year', 'month', 'host_kind', 'path_kind', 'protocol',
                  'method', 'status', 'size_min', 'size_max', 'size_avg',
                  'referer_kind', 'ua_kind', 'total', 'source')

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
