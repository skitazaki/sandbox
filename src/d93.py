#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Double Squares
# http://stackoverflow.com/questions/4632037/double-squares-problem

import math

# facebook hackers cup, 2011
inputs = """20
372654318
801125
421330820
138125
1022907856
1041493518
3
1096354453
473200074
2147483647
415485223
326864818
1077003976
713302969
1740798996
1148284322
10
5525
4005625
4225
"""


def parse_inputs(inputs):
    candidats = [int(l) for l in inputs.split("\n") if l][1:]
    candidats.sort()
    return candidats


def resolver(candidats, reputation_limit=100):
    ret = {}
    for r in candidats:
        ret[r] = 0

    cached = {}
    for i in range(reputation_limit):
        cached[i] = i * i

    for c1 in range(reputation_limit):
        m = candidats[0]
        if m < cached[c1]:
            if len(candidats) == 1:
                return ret
            candidats = candidats[1:]
            print "Removed %d" % m
        for c2 in range(c1, reputation_limit):
            c = cached[c1] + cached[c2]
            if c > candidats[-1]:
                break
            if c in candidats:
                print "%d^2 + %d^2 = %d" % (c1, c2, c)
                ret[c] += 1
    return ret


def main():
    candidats = parse_inputs(inputs)
    max_cand = candidats[-1]
    sq = math.sqrt(max_cand)
    rt = int(math.ceil(sq))
    print "max=%d, sqrt=%f, limit=%d" % (max_cand, sq, rt)
    import time
    start = time.time()
    ret = resolver(candidats, rt)
    print "time: %d" % (time.time() - start)
    print "\n".join(["%15d: %d" % (k, ret[k]) for k in ret])

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
