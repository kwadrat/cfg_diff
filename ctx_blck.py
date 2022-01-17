#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Detect block of lines between two specified markers
'''

import unittest


def dtct_blk(marker_start, marker_end, line_ls):
    result = None
    if line_ls:
        try:
            first_index = line_ls.index(marker_start)
            last_index = line_ls.index(marker_end, first_index)
            result = (first_index, last_index)
        except ValueError:
            pass
    return result


class TestContextBlock(unittest.TestCase):
    def test_context_block(self):
        '''
        TestContextBlock:
        '''
        self.assertEqual(dtct_blk('a', 'b', []), None)
        self.assertEqual(dtct_blk('a', 'b', ['a', 'b']), (0, 1))
        self.assertEqual(dtct_blk('a', 'b', ['a', 'c', 'b']), (0, 2))
        self.assertEqual(dtct_blk('a', 'b', ['d', 'a', 'c', 'b']), (1, 3))
        self.assertEqual(dtct_blk('a', 'b', ['d', 'a', 'c', 'b', 'e']), (1, 3))
        self.assertEqual(dtct_blk('a', 'b', ['b', 'd', 'a', 'c', 'b', 'e']), (2, 4))
        self.assertEqual(dtct_blk('a', 'b', ['b', 'd', 'c', 'b', 'e']), None)
        self.assertEqual(dtct_blk('a', 'b', ['b', 'd', 'a', 'c', 'e']), None)
