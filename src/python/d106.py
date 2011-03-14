#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Converter script to rename J-League club name.
"""

import os.path
import sys

_MAPPER = u'''
ベガルタ仙台,仙台
モンテディオ山形,山形
鹿島アントラーズ,鹿島
浦和レッズ,浦和
大宮アルディージャ,大宮
柏レイソル,柏
川崎フロンターレ,川崎Ｆ
横浜F.マリノス,横浜FM
ヴァンフォーレ甲府,甲府
アルビレックス新潟,新潟
清水エスパルス,清水
ジュビロ磐田,磐田
名古屋グランパス,名古屋
ガンバ大阪,Ｇ大阪
セレッソ大阪,Ｃ大阪
ヴィッセル神戸,神戸
サンフレッチェ広島,広島
アビスパ福岡,福岡
コンサドーレ札幌,札幌
水戸ホーリーホック,水戸
栃木SC,栃木
ザスパ草津,草津
ジェフユナイテッド市原・千葉,千葉
FC東京,Ｆ東京
東京ヴェルディ,東京Ｖ
横浜FC,横浜FC
湘南ベルマーレ,湘南
カターレ富山,富山
FC岐阜,岐阜
京都サンガ,京都
ガイナーレ鳥取,鳥取
ファジアーノ岡山,岡山
徳島ヴォルティス,徳島
愛媛FC,愛媛
ギラヴァンツ北九州,北九州
サガン鳥栖,鳥栖
ロアッソ熊本,熊本
大分トリニータ,大分
'''

MAPPER = {}
for line in _MAPPER.strip().split('\n'):
    ret, candidates = line.split(',')
    MAPPER[ret] = candidates


def mapper(line):
    s = line
    for ret, candidates in MAPPER.iteritems():
        s = s.replace(candidates, ret)
    return s


def converter(f, stream, writer):
    for line in stream:
        writer.write(f(line))


def main():
    if len(sys.argv) != 2:
        print >>sys.stderr, "Give me file name from argument."
        sys.exit(1)
    fname = sys.argv[1]
    if not os.path.exists(fname):
        print >>sys.stderr, fname, "is not found."
        sys.exit(1)

    input = open(fname, 'rb')
    output = sys.stdout
    converter(mapper, input, output)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
