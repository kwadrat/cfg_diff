#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Test single period changes
'''

import unittest

import tx_place


def both_starts(a_txt, b_txt, common_txt):
    result = 0
    if a_txt.startswith(common_txt) and b_txt.startswith(common_txt):
        result = 1
    return result


class MultiReplacer(object):
    def __init__(self, good_ls=None):
        '''
        MultiReplacer:
        '''
        if good_ls is None:
            self.good_ls = [
                tx_place.sta_8_tement,
                tx_place.sta_7_tement,
                ]
        else:
            self.good_ls = good_ls

    def process_replace(self, fa, fb, As, Ae, Bs, Be):
        '''
        MultiReplacer:
        '''
        needs_work = 1
        delta_a = Ae - As
        if delta_a == Be - Bs:
            diff_cnt = 0
            suspicious_change = 0
            for i in range(delta_a):
                part_a = fa[As + i]
                part_b = fb[Bs + i]
                if part_a != part_b:
                    diff_cnt += 1
                    if not any(map(lambda x: both_starts(part_a, part_b, x), self.good_ls)):
                        suspicious_change = 1
            if diff_cnt <= 2 and not suspicious_change:
                needs_work = 0
        return needs_work


class TestSinglePeriod(unittest.TestCase):
    def test_equal_length(self):
        '''
        TestSinglePeriod:
        '''
        multi_replacer = MultiReplacer()
        fa = []
        fb = []
        As = 0
        Ae = 0
        Bs = 0
        Be = 0
        self.assertEqual(multi_replacer.process_replace(fa, fb, As, Ae, Bs, Be), 0)

    def test_too_many_differences(self):
        '''
        TestSinglePeriod:
        '''
        multi_replacer = MultiReplacer()
        fa = ['a', 'b']
        fb = ['c', 'd']
        As = 0
        Ae = 2
        Bs = 0
        Be = 2
        self.assertEqual(multi_replacer.process_replace(fa, fb, As, Ae, Bs, Be), 1)

    def test_wrong_change(self):
        '''
        TestSinglePeriod:
        '''
        multi_replacer = MultiReplacer()
        fa = ['a', 'b']
        fb = ['c', 'b']
        As = 0
        Ae = 2
        Bs = 0
        Be = 2
        self.assertEqual(multi_replacer.process_replace(fa, fb, As, Ae, Bs, Be), 1)

    def test_common_prefix(self):
        '''
        TestSinglePeriod:
        '''
        self.assertEqual(both_starts('', '', ''), 1)
        self.assertEqual(both_starts('', '', 'a'), 0)
        self.assertEqual(both_starts('x', 'x', 'a'), 0)
        self.assertEqual(both_starts('a', 'a', 'a'), 1)
