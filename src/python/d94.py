#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Peg Games, timeup:(

import sys


def parse_inputs(stream):
    candidats = []
    for l in stream:
        t = [int(f) for f in l.split(" ") if f]
        candidats.append(t)
    return candidats[1:]


def resolver(inputs):
    ret = {}
    for game in inputs:
        row = game[0]
        column = game[1]
        goal = game[2]
        panel = []
        for r in range(row):
            c = column
            if r % 2 == 1:
                c = column - 1
            panel.append([True for _ in range(c)])
        for i in range(game[3]):
            f = 4 + i * 2
            panel[game[f]][game[f + 1]] = False

        print "-" * 80
        writer = sys.stdout
        r = 0
        for line in panel:
            if r % 2 == 1:
                writer.write(" ")
            for f in line:
                if f:
                    writer.write("X")
                else:
                    writer.write(" ")
                writer.write(" ")
            r += 1
            writer.write("\n")
        writer.write(" ")
        writer.write(" " * goal * 2)
        writer.write("G\n")

    return ret


def main():
    fname = sys.argv[1]
    inputs = parse_inputs(open(fname))
    print "count=%d" % (len(inputs),)
    import time
    start = time.time()
    ret = resolver(inputs)
    print "time: %d" % (time.time() - start)
    print "\n".join(["%15d: %d" % (k, ret[k]) for k in ret])

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
