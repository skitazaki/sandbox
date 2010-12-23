#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Sample usage of ``spawnProcess`` of Twisted.
# example: $ python d62.py
# see http://twistedmatrix.com/pipermail/twisted-python/2010-August/022758.html

from twisted.internet import reactor, protocol


class ProcessPrinter(protocol.ProcessProtocol):

    def connectionMade(self):
        print "::connectionMade"

    def outReceived(self, data):
        print "::outReceived"
        print data

    def errReceived(self, data):
        print "::errReceived"
        print data

    def processEnded(self, status_object):
        print "::processEnded"
        print "exit code %d" % status_object.value.exitCode
        reactor.stop()


def spawn_after_run():
    argv = ['/opt/local/bin/git', 'clone', 'git://git.gnome.org/gimp']
    reactor.spawnProcess(ProcessPrinter(), argv[0], argv)

reactor.callLater(0, spawn_after_run)
reactor.run()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
