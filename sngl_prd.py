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


def process_replace(fa, fb, As, Ae, Bs, Be):
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
                if both_starts(part_a, part_b, tx_place.sta_8_tement):
                    pass
                elif both_starts(part_a, part_b, tx_place.sta_7_tement):
                    pass
                else:
                    suspicious_change = 1
        if diff_cnt <= 2 and not suspicious_change:
            needs_work = 0
    return needs_work


class MultiReplacer(object):
    def __init__(self):
        '''
        MultiReplacer:
        '''

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
                    if both_starts(part_a, part_b, tx_place.sta_8_tement):
                        pass
                    elif both_starts(part_a, part_b, tx_place.sta_7_tement):
                        pass
                    else:
                        suspicious_change = 1
            if diff_cnt <= 2 and not suspicious_change:
                needs_work = 0
        return needs_work


class TestSinglePeriod(unittest.TestCase):
    def test_equal_length(self):
        '''
        TestSinglePeriod:
        '''
        fa = []
        fb = []
        As = 0
        Ae = 0
        Bs = 0
        Be = 0
        self.assertEqual(process_replace(fa, fb, As, Ae, Bs, Be), 0)

    def test_too_many_differences(self):
        '''
        TestSinglePeriod:
        '''
        fa = ['a', 'b']
        fb = ['c', 'd']
        As = 0
        Ae = 2
        Bs = 0
        Be = 2
        self.assertEqual(process_replace(fa, fb, As, Ae, Bs, Be), 1)

    def test_wrong_change(self):
        '''
        TestSinglePeriod:
        '''
        fa = ['a', 'b']
        fb = ['c', 'b']
        As = 0
        Ae = 2
        Bs = 0
        Be = 2
        self.assertEqual(process_replace(fa, fb, As, Ae, Bs, Be), 1)

    def test_common_prefix(self):
        '''
        TestSinglePeriod:
        '''
        self.assertEqual(both_starts('', '', ''), 1)
        self.assertEqual(both_starts('', '', 'a'), 0)
        self.assertEqual(both_starts('x', 'x', 'a'), 0)
        self.assertEqual(both_starts('a', 'a', 'a'), 1)
