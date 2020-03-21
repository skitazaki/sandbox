#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Wrapper script for `api.cybozulive.com`.

:Author: KITAZAKI Shigeru
:Version: 0.4
"""

from datetime import timedelta
import logging

# http://diveintopython3.org/xml.html
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

from util import NOW
import models

OPTIONAL_HEADER_NAME = 'X-Cybozu-Status-Code'

# Test use.
_INTERNAL_DEVELOPMENT = False
if _INTERNAL_DEVELOPMENT:
    REQUEST_TOKEN_URL = 'http://localhost/oauth/initiate'
    ACCESS_TOKEN_URL = 'http://localhost/oauth/token'
    AUTHORIZATION_URL = 'http://localhost/oauth/authorize'
    TEMPLATE_URL = 'http://localhost/api/%s/V2'
else:
    REQUEST_TOKEN_URL = 'https://api.cybozulive.com/oauth/initiate'
    ACCESS_TOKEN_URL = 'https://api.cybozulive.com/oauth/token'
    AUTHORIZATION_URL = 'https://api.cybozulive.com/oauth/authorize'
    TEMPLATE_URL = 'https://api.cybozulive.com/api/%s/V2'

XAUTH_ENABLE = False

ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom'
CYBOZULIVE_COMMON_NAMESPACE = 'http://schemas.cybozulive.com/common/2010'
CYBOZULIVE_SCHEDULE_NAMESPACE = 'http://schemas.cybozulive.com/schedule/2010'
CYBOZULIVE_NOTIFICATION_NAMESPACE = 'http://schemas.cybozulive.com/notification/2010'


class CybozuliveException(Exception):
    pass


class Entry(models.Model):
    """Base class to represents one item such "atom:entry"."""

    id = None
    title = None
    content = None
    summary = None
    published = None
    author = None
    link = None
    updated = None


class Notification(Entry):

    status = None
    group = None


class Task(Entry):

    group = None


class Schedule(Entry):

    group = None


class Comment(Entry):

    parent = None


class Board(Entry):

    group = None


class Group(Entry):

    pass


def process(r, Entity):

    def mapper(elements):
        ret = Entity()
        for e in elements:
            if e.tag.startswith('{%s}' % (ATOM_NAMESPACE,)):
                t = e.tag[len(ATOM_NAMESPACE) + 2:]
                if t == 'author':
                    uri = e.find('{%s}uri' % (ATOM_NAMESPACE,))
                    name = e.find('{%s}name' % (ATOM_NAMESPACE,))
                    ret.author = name.text
                elif t == 'link' and e.get('rel') == 'alternate':
                    ret.link = e.get('href')
                elif hasattr(ret, t) and e.text:
                    setattr(ret, t, e.text)
            elif e.tag.startswith('{%s}' % (CYBOZULIVE_COMMON_NAMESPACE,)):
                t = e.tag[len(CYBOZULIVE_COMMON_NAMESPACE) + 2:]
                if t in ('who', 'when', 'attachment', 'group',
                        'facility', 'task'):
                    #data[t].append((e.get('id'), e.get('valueString')))
                    pass
                elif hasattr(ret, t) and e.text:
                    setattr(ret, t, e.text)
                else:
                    logging.info("Unknown tag %s" % (e.tag,))
            elif e.tag.startswith('{%s}' % (CYBOZULIVE_NOTIFICATION_NAMESPACE,)):
                t = e.tag[len(CYBOZULIVE_NOTIFICATION_NAMESPACE) + 2:]
                if t in ('mailNotified', 'icon'):
                    pass
            elif e.tag.startswith('{%s}' % (CYBOZULIVE_SCHEDULE_NAMESPACE,)):
                t = e.tag[len(CYBOZULIVE_SCHEDULE_NAMESPACE) + 2:]
            else:
                logging.info("Unknown tag %s" % (e.tag,))
        return ret

    feed = etree.fromstring(r)
    items = []
    for elem in feed.getchildren():
        if elem.tag == '{%s}entry' % (ATOM_NAMESPACE,):
            item = mapper(elem.getchildren())
            items.append(item)
    return items


class Api(object):
    """Accessor for "api.cybozulive.com"."""

    def __init__(self, client):
        self.client = client

    def access(self, entity, params=None, data=None):
        """Transport method to issue HTTP request with given parameters.
        Args:
        * entity - string or Entity object.
        * params - dict for request header.
        * data - string to send on HTTP body.
        Return:
        * urllib2.Response
        """
        if type(entity) is str:
            target = entity
            entity = Entry
        elif hasattr(entity, '__name__'):
            target = entity.__name__.lower()
        else:
            raise CybozuliveException("Unknown target entity, %s" % (repr(entity),))
        url = TEMPLATE_URL % (target,)
        try:
            resource = self.client.access(url, params, data)
            r = resource.read()
            logging.debug(r)
            # `getcode()` is available since Python 2.6.
            st = 200
            if 'getcode' in resource.__dict__:
                st = resource.getcode()
            headers = resource.info()
            if OPTIONAL_HEADER_NAME in headers:
                s = int(headers[OPTIONAL_HEADER_NAME])
                if st != s:
                    raise IOError("HTTP Status: %d, %s: %d\n%s" %
                            (st, OPTIONAL_HEADER_NAME, s, r))
            return process(r, entity)
        except IOError, e:
            logging.error(repr(e))

    def notification(self, params=None, confirm=None, sync=False):
        """Manage notification information.
        Args:
        * params
        * confirm
        * sync
        """
        data = None
        if confirm:
            if type(confirm) is not list:
                confirm = list(confirm)
            feed = etree.Element('{%s}feed' % (ATOM_NAMESPACE, ))
            for e in confirm:
                entry = create_entry(id=e.id, updated=e.updated)
                feed.append(entry)
            data = etree.tostring(feed)

        return self.access(Notification, params, data)

    def schedule(self, params=None, event=None, sync=False):
        """Manage schedule.
        Args:
        * params
        * event
        * sync
        """
        if confirms:
            print "Request confirmation request,", confirms

        return self.access(Schedule, params)

    def task(self, params=None, task=None):
        """Manage task.
        Args:
        * params
        * task
        """
        if task:
            print "Request confirmation request,", task

        return self.access(Task, params)

    def board(self, group, params=None, topic=None, operation=None):
        """Manage discussion board topic.
        Args:
        * group
        * params
        * topic
        * operation
        """
        data = None
        if topic:
            entity = Board
            # `operation` are insert, update, delete, and query.
            feed = etree.Element('{%s}feed' % (ATOM_NAMESPACE, ))
            op = etree.Element('{%s}%s' % (CYBOZULIVE_COMMON_NAMESPACE, 'operation'))
            # TODO: it seems better to use 'content' instead of 'summary'.
            if topic.id:
                entry = create_entry(id=topic.id, title=topic.title, summary=topic.summary)
                if topic.title:
                    op.set('type', 'UPDATE')
                else:
                    op.set('type', 'DELETE')
            else:
                entry = create_entry(title=topic.title, summary=topic.summary)
                e = etree.Element('{%s}%s' % (CYBOZULIVE_COMMON_NAMESPACE, 'group'))
                e.set('id', group)
                entry.append(e)
                op.set('type', 'INSERT')
            feed.append(op)
            feed.append(entry)
            data = etree.tostring(feed, encoding='utf-8')

        if params is None:
            params = dict()
        params['group'] = group
        return self.access(Board, params, data)

    def group(self, params=None):
        """Manage group information.
        Args:
        * params
        """
        return self.access(Group, params)

    def comment(self, params=None, comment=None, operation=None):
        """Manage comment for each item.
        Args:
        * params
        * comment
        * operation
        """
        entity = Comment
        data = None
        if comment:
            feed = etree.Element('{%s}feed' % (ATOM_NAMESPACE, ))
            entry = None
            if not params:
                params = {}
            if comment.parent:
                # Add comment.
                entity = comment.parent.__class__
                e = etree.Element('{%s}id' % (ATOM_NAMESPACE, ))
                e.text = comment.parent.id
                feed.append(e)
                c = comment.content if comment.content else comment.summary
                # TODO: it seems better to use 'content' instead of 'summary'.
                entry = create_entry(summary=comment.summary)
                feed.append(entry)
                e = etree.Element('{%s}%s' % (CYBOZULIVE_COMMON_NAMESPACE, 'operation'))
                e.set('type', 'insert')
                feed.append(e)
            elif comment.id:
                # Delete comment.
                entry = create_entry(id=comment.id)
                e = etree.Element('{%s}%s' % (CYBOZULIVE_COMMON_NAMESPACE, 'operation'))
                e.set('type', 'delete')
                feed.append(e)
            else:
                raise CybozuliveException("Invalid object.")
            feed.append(entry)
            data = etree.tostring(feed, encoding='utf-8')

        return self.access(entity, params, data)

    def initialize(self):
        """Get access token along with OAuth dance or xAuth."""
        if XAUTH_ENABLE:
            endpoints = (ACCESS_TOKEN_URL,)
        else:
            endpoints = (REQUEST_TOKEN_URL,
                    AUTHORIZATION_URL, ACCESS_TOKEN_URL)
        try:
            ret = self.client.initialize(endpoints)
            return ret
        except IOError, e:
            logging.error(repr(e))


def run_sample(api):
    # any tests are appreciated.
    test_read(api)
    #test_write(api)
    #test_sync(api)
    #test_delete(api)


def test_star(api):
    stars = api.access('star')
    for star in stars:
        print repr(star)

    target = 'GROUP,1:1,GW_SCHEDULE,1:1'
    feed = etree.Element('{%s}feed' % (ATOM_NAMESPACE, ))
    op = etree.Element('{%s}operation' % (CYBOZULIVE_COMMON_NAMESPACE, ))
    op.set('type', 'INSERT')
    feed.append(op)
    entry = create_entry(id=target)
    feed.append(entry)
    api.access('star', data=etree.tostring(feed))

    feed = etree.Element('{%s}feed' % (ATOM_NAMESPACE, ))
    op = etree.Element('{%s}operation' % (CYBOZULIVE_COMMON_NAMESPACE, ))
    op.set('type', 'DELETE')
    feed.append(op)
    entry = create_entry(id=target)
    feed.append(entry)
    api.access('star', data=etree.tostring(feed))


def test_read(api):
    import codecs
    writer = codecs.open('cybozulive.txt', 'w+', encoding='utf-8')

    def printer(item):
        print >>writer, "-" * 79
        print >>writer, "%s (%s) %s - %s" % (item.title, item.id,
            item.updated, item.author)
        print >>writer, '    <%s>' % (item.link,)
        if hasattr(item, 'when') and item.when:
            print >>writer, "\n".join(["%s to %s" % w for w in item.when])
        if hasattr(item, 'who') and item.who:
            print >>writer, "%s" % (item.who,)
        if hasattr(item, 'group') and item.group:
            print >>writer, "GROUP: %s, %s" % item.group[0]
        if item.summary:
            print >>writer, item.summary

    #headlines = api.notification()
    #for item in headlines:
    #    printer(item)

    headlines = api.notification({'unconfirmed': True})
    for item in headlines:
        printer(item)
        ret = models.find(Notification, id=item.id)
        if ret is None:
            item.put()

    #headlines = api.notification({'category': 'MEMBER_LIST'})
    #for item in headlines:
    #    printer(item)

    tasks = api.task()
    for item in tasks:
        printer(item)

    tasks = api.task({'embed-comment': True})
    for item in tasks:
        printer(item)

    tasks = api.task({'embed-comment': True, 'group': '1:1'})
    for item in tasks:
        printer(item)

    events = api.schedule()
    for item in events:
        printer(item)

    events = api.schedule({'embed-comment': True})
    for item in events:
        printer(item)

    topics = api.board('1:1')
    assert topics is None

    topics = api.board('1:1', {'embed-comment': True})
    assert topics is None

    #groups = api.group()
    #for item in groups:
    #    printer(item)

    # under construction.
    #comments = api.comment()
    #for item in comments:
    #    printer(item)

    #comments = api.comment({'item': 'GROUP,1:1,BOARD,1:1'})
    #for item in comments:
    #    printer(item)

    writer.close()

    #for i in range(9):
    #    logging.debug("i=%d" % (i,))
    #    api.access("schedule", {"group": "1:1",
    #        "start-index":i * 20,
    #        "embed-comment": True,
    #        "term-start": "2010-01-01",
    #        "term-end": "2010-12-31"})
    # Response is too large :(
    #api.access("board", {"group": "1:1", "embed-comment": True})


def create_entry(**kwargs):
    entry = etree.Element('{%s}entry' % (ATOM_NAMESPACE,))
    for k, v in kwargs.iteritems():
        e = etree.Element('{%s}%s' % (ATOM_NAMESPACE, k))
        e.text = v
        entry.append(e)
    return entry


def test_write(api):
    """POST method for cybozulive.com"""
    # Confirm single item.
    n = Notification(id='GROUP,1:1,BOARD,1:1',
            updated=NOW.strftime('%Y-%m-%dT%H:%M:%SZ'))
    #api.notification(confirm=n)
    # Confirm multiple items.
    #api.notification(confirm=[Notification(id='GROUP,1:1,CABINET,1:1'),
    #    Notification(id='GROUP,1:1,TASK,1:1')])

    # create a new topic!! it has not id yet.
    for i in range(2):
        delta = timedelta(i)
        n = (NOW - delta).strftime("%Y-%m-%dT%H:%M:%SZ")
        topic = Board(title=u"No.%d: API 経由での投稿です" % (i + 1,),
                    summary=u"いろはにほへと" +
                        u"ちりぬるを わかよたれそ" +
                        u"つねならむ ういのおくやま けふこえて" +
                        u"あさきゆめみし えいもせず",
                    updated=n)
        api.board("1:1", topic=topic)

    # create comment on specific item.
    c = Comment(parent=Board(id='GROUP,1:1,BOARD,1:1'),
            summary=u"コメント書き込みAPIのテストです。")
    api.comment(comment=c)

    # edit a existing item.
    topic = Board(id='GROUP,1:1,BOARD,1:1',
                title=u"API 経由で変更しました",
                summary=u"あいうえお",
                updated=NOW.strftime("%Y-%m-%dT%H:%M:%SZ"))
    api.board("1:1", topic=topic)


def test_delete(api):
    # delete a comment.
    c = Comment(id='GROUP,1:1,BOARD,1:1,COMMENT,1')
    api.comment(comment=c)
    c = Comment(id='GROUP,1:1,BOARD,1:1,COMMENT,2')
    api.comment(comment=c)


def test_sync(api):
    """Experimental method for cybozulive.com"""
    n = NOW.strftime("%Y-%m-%dT%H:%M:%SZ")
    data = [
        ["GROUP,1:1,GW_SCHEDULE,1:1", n],
        ["GROUP,1:1,GW_SCHEDULE,1:2", n],
        ["GROUP,1:2,GW_SCHEDULE,1:10", n],
        ["MYPAGE,1:1,MP_SCHEDULE,1:1", n],
        ["MYPAGE,1:1,MP_SCHEDULE,1:2", n]]

    feed = etree.Element('{%s}feed' % (ATOM_NAMESPACE, ))
    title = etree.Element('{%s}title' % (ATOM_NAMESPACE, ))
    title.text = 'DIFF'
    feed.append(title)

    for item in data:
        entry = create_entry(id=item[0], updated=item[1])
        feed.append(entry)
        # TODO: use this entity instead of calling access() directly.
        e = Schedule(id=item[0], updated=item[1])
    api.access("scheduleSync", data=etree.tostring(feed))

    data = [
        ["GROUP,1:1,GW_SCHEDULE,1:1", "CREATED"],
        ["GROUP,1:1,GW_SCHEDULE,1:2", "NOTFOUND"],
        ["GROUP,1:2,GW_SCHEDULE,1:10", "UPDATED"]]

    feed = etree.Element('{%s}feed' % (ATOM_NAMESPACE, ))
    title = etree.Element('{%s}title' % (ATOM_NAMESPACE, ))
    title.text = 'SYNC'
    feed.append(title)

    for item in data:
        entry = create_entry(id=item[0], title=item[1])
        feed.append(entry)
        # TODO: use this entity instead of calling access() directly.
        e = Schedule(id=item[0], updated=item[1])
    api.access("scheduleSync", data=etree.tostring(feed))

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
