#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Select only subset of lines in first list
'''

import unittest


def source_limits(one_txt):
    result = None
    if one_txt:
        all_parts = one_txt.split('-')
        if all_parts[0]:
            a_value = int(all_parts[0])
        else:
            a_value = None
        if len(all_parts) == 2:
            if all_parts[1]:
                b_value = int(all_parts[1])
            else:
                b_value = None
        if len(all_parts) == 1:
            b_value = a_value
        result = (a_value, b_value)
    return result


class LineAcceptor(object):
    def __init__(self, one_text=None):
        '''
        LineAcceptor:
        '''
        source_ls = source_limits(one_text)
        self.is_null = source_ls is None
        if not self.is_null:
            self.limit_a, self.limit_b = source_ls

    def is_ok(self, one_line):
        '''
        LineAcceptor:
        '''
        result = 1
        if not self.is_null:
            if self.limit_a is not None and one_line < self.limit_a:
                result = 0
            if self.limit_b is not None and one_line > self.limit_b:
                result = 0
        return result


class TestFocusedLines(unittest.TestCase):
    def test_focused_lines(self):
        '''
        TestFocusedLines:
        '''
        self.assertEqual(source_limits(None), None)
        self.assertEqual(source_limits('1'), (1, 1))
        self.assertEqual(source_limits('2'), (2, 2))
        self.assertEqual(source_limits('2-5'), (2, 5))
        self.assertEqual(source_limits('3-'), (3, None))
        self.assertEqual(source_limits('-7'), (None, 7))

    def test_as_object(self):
        '''
        TestFocusedLines:
        '''
        obj = LineAcceptor()
        self.assertEqual(obj.is_ok(1), 1)
        obj = LineAcceptor('2')
        self.assertEqual(obj.is_ok(1), 0)
        self.assertEqual(obj.is_ok(2), 1)
        self.assertEqual(obj.is_ok(3), 0)
        obj = LineAcceptor('4-')
        self.assertEqual(obj.is_ok(4), 1)
        obj = LineAcceptor('-7')
        self.assertEqual(obj.is_ok(6), 1)
