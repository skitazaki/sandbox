# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.utils.log import getLogger
from django.utils import timezone
import datetime
import itertools
from collections import Counter, defaultdict
from optparse import make_option
import dateutil.relativedelta
import dateutil.parser
from accesslog.models import (
    AccessLog,
    MinuteSummary,
    HourSummary,
    DaySummary,
    MonthSummary
)

DATETIME_FMT = '%Y-%m-%d %H:%M:%S'


class AggregateAction(object):

    def __init__(self, source):
        self.source = source
        self.logger = getLogger(__name__)
        self.tz = timezone.get_current_timezone()

    def to_localtime(self, time):
        local_time = self.tz.normalize(time.astimezone(self.tz))
        return local_time

    def aggregate(self, elements):
        counter = defaultdict(Counter)
        size = []
        for e in elements:
            counter['host'][e.host] += 1
            counter['path'][e.path] += 1
            counter['protocol'][e.protocol] += 1
            counter['method'][e.method] += 1
            counter['status'][e.status] += 1
            counter['referer'][e.referer] += 1
            counter['ua'][e.ua] += 1
            if e.size:
                size.append(e.size)
        if len(size) > 0:
            counter['size']['min'] = min(size)
            counter['size']['max'] = max(size)
            counter['size']['avg'] = sum(size) / len(size)
        return counter

    def transform(self, counter):
        stats = {
            'total': sum(counter['status'].values()),
            'host_kind': len(counter['host'].keys()),
            'path_kind': len(counter['path'].keys()),
            'size_min': counter['size'].get('min'),
            'size_max': counter['size'].get('max'),
            'size_avg': counter['size'].get('avg'),
            'referer_kind': len(counter['referer'].keys()),
            'ua_kind': len(counter['ua'].keys()),
            'status': counter['status'],
            'protocol': counter['protocol'],
            'method': counter['method'],
        }
        return stats

    def make_query(self, start, end):
        self.logger.info('Make query to fetch records between (%s , %s) [%s]',
                         start.strftime(DATETIME_FMT),
                         end.strftime(DATETIME_FMT),
                         self.source)
        q = AccessLog.objects.all().filter(source=self.source).\
            filter(time__gte=start, time__lt=end).\
            order_by('source', 'time')
        return q

    def daysummary(self, start, end):
        q = self.make_query(start, end)
        for k, el in itertools.groupby(q, key=lambda x: (x.source, self.to_localtime(x.time).date())):  # noqa
            source, day = k
            self.logger.info('Start aggregating: [{}] {}'.format(
                source, day.strftime('%Y-%m-%d')))
            counter = self.aggregate(el)
            stats = self.transform(counter)
            obj, created = DaySummary.objects.get_or_create(
                source=source, day=day, defaults=stats)
            if created:
                self.logger.debug('Created a new row on database.')

    def hoursummary(self, start, end):
        q = self.make_query(start, end)
        for k, el in itertools.groupby(q, key=lambda x: (x.source, self.to_localtime(x.time).date(), self.to_localtime(x.time).hour)):  # noqa
            source, day, hour = k
            self.logger.info('Start aggregating: [{}] {} {}'.format(
                source, day, hour))
            counter = self.aggregate(el)
            stats = self.transform(counter)
            obj, created = HourSummary.objects.get_or_create(
                source=source, day=day, hour=hour, defaults=stats)
            if created:
                self.logger.debug('Created a new row on database.')

    def monthsummary(self, start, end):
        q = self.make_query(start, end)
        for k, el in itertools.groupby(q, key=lambda x: (x.source, self.to_localtime(x.time).year, self.to_localtime(x.time).month)):  # noqa
            source, year, month = k
            self.logger.info('Start aggregating: [{}] {}/{}'.format(
                source, year, month))
            counter = self.aggregate(el)
            stats = self.transform(counter)
            obj, created = MonthSummary.objects.get_or_create(
                source=source, year=year, month=month, defaults=stats)
            if created:
                self.logger.debug('Created a new row on database.')

    def minutesummary(self, start, end):
        q = self.make_query(start, end)
        for k, el in itertools.groupby(q,
                key=lambda x: (x.source, x.time.replace(second=0, microsecond=0))):  # noqa
            source, time = k
            self.logger.info('Start aggregating: [{}] {}'.format(
                source, time.strftime(DATETIME_FMT)))
            counter = self.aggregate(el)
            stats = self.transform(counter)
            obj, created = MinuteSummary.objects.get_or_create(
                source=source, time=time, defaults=stats)
            if created:
                self.logger.debug('Created a new row on database.')


dispatcher = {
    'minute': 'minutesummary',
    'hour': 'hoursummary',
    'day': 'daysummary',
    'month': 'monthsummary'
}


class Command(BaseCommand):

    help = 'Make time resampling summary'

    option_list = BaseCommand.option_list + (
        make_option('--source', dest='source',
                    default='<stdin>',
                    help='Log records source marker.'),
        make_option('--action', dest='action',
                    choices=tuple(dispatcher.keys()), default='minute',
                    help='Action to dispatch.'),
        make_option('--start', dest='start',
                    help='Start to make summary.'),
        make_option('--end', dest='end',
                    help='End to make summary.'),
        )

    def handle(self, *args, **options):
        action = AggregateAction(options['source'])

        # Set term to make summary.
        start, end = None, None
        if options['start']:
            start = dateutil.parser.parse(options['start'])
        if options['end']:
            end = dateutil.parser.parse(options['end'])
        if start is None:
            if end is None:
                end = datetime.datetime.now()
            start = end + dateutil.relativedelta.relativedelta(months=-1)
        else:
            if end is None:
                end = start + dateutil.relativedelta.relativedelta(months=+1)
        if start >= end:
            msg = 'End has to be after start. start={}, end={}'
            raise CommandError(msg.format(
                start.strftime(DATETIME_FMT), end.strftime(DATETIME_FMT)))

        # Dispatch the action.
        prop = dispatcher.get(options['action'])
        if prop is None:
            raise CommandError('Unknown action: {}'.format(options['action']))
        func = getattr(action, prop)
        if func is None:
            raise CommandError('Function is missing: {}'.format(prop))
        return func(start, end)

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
