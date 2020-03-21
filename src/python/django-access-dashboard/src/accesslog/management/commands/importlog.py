from django.core.management.base import BaseCommand, CommandError
from django.utils.log import getLogger
from django.db.utils import IntegrityError
import gzip
import json
import os
import sys
from optparse import make_option
import clitool.accesslog
import dateutil.parser
import dateutil.tz
from accesslog.models import AccessLog


class AccessLogImport(object):

    def __init__(self, parser, source=None):
        self.parser = parser
        self.source = source
        self.logger = getLogger(__name__)

    def import_all(self, stream):
        for l in map(str.rstrip, stream):
            r = self.parser(l)
            if r is None:
                self.logger.error('Fail to parse: %s', l)
                continue
            m = AccessLog(
                time=r['time'],
                host=r['host'],
                path=r['path'],
                query=r['query'],
                method=r['method'],
                protocol=r['protocol'],
                status=r['status'],
                size=r.get('size'),
                referer=r.get('referer'),
                ua=r.get('ua'),
                ident=r.get('indent'),
                user=r.get('user'),
                trailing=r.get('trailing'),
                source=r.get('source', self.source)
            )
            try:
                m.save()
            except IntegrityError as e:
                self.logger.error(e)
                self.logger.error(' -- %s', l)


def parse_raw(line):
    r = clitool.accesslog.parse(line)
    tz = dateutil.tz.tzoffset(None, r['utcoffset'].total_seconds())
    r['time'] = r['time'].replace(tzinfo=tz)
    return r


def parse_fluentd(line):
    time, tag, dt = line.split('\t')
    data = json.loads(dt)
    if 'path' in data:
        s = data['path'].split('?', 1)  # Split path and query
        if len(s) == 2:
            p, q = s
        else:
            p, q = s[0], None
    else:
        p, q = None, None
    size = int(data['size']) if data.get('size', '').isdigit() else None
    return {
        'time': dateutil.parser.parse(time), 'host': data['host'],
        'path': p, 'query': q,
        'method': data['method'], 'protocol': 'HTTP',
        'status': int(data['code']), 'size': size,
        'referer': data['referer'] if data['referer'] != '-' else None,
        'ua': data['agent'] if data['agent'] != '-' else None,
        'ident': data.get('ident'),
        'user': data.get('user') if data.get('user') != '-' else None,
        'source': tag
    }


PARSER_MAPPING = {
    'raw': parse_raw,
    'fluentd': parse_fluentd
}


class Command(BaseCommand):

    help = 'Import access log'

    option_list = BaseCommand.option_list + (
        make_option('--source',
            dest='source',
            help='Log records source marker.'),
        make_option('--parser',
            dest='parser',
            choices=tuple(PARSER_MAPPING.keys()),
            default='raw',
            help='Parser type.'),
        )

    def handle(self, *args, **options):
        parser = PARSER_MAPPING[options['parser']]
        p = AccessLogImport(parser, options['source'])
        if args:
            for fname in args:
                if not os.path.exists(fname):
                    raise CommandError('File not found: {}'.format(fname))
                _, ext = os.path.splitext(fname)
                if ext == '.gz':
                    opener = lambda f: gzip.open(f, 'rt')  # Text mode.
                else:
                    opener = open
                with opener(fname) as fp:
                    p.import_all(fp)
        else:
            if options['source'] is None:
                p.source = '<stdin>'
            p.import_all(sys.stdin)

