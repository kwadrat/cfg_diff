#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Define labels for changing sets of lines
'''

import unittest


LBL_EQUAL = 'equal'
LBL_INSERT = 'insert'
LBL_REPLACE = 'replace'


class TestPreparedLabels(unittest.TestCase):
    def test_prepared_labels(self):
        '''
        TestPreparedLabels:
        '''
        self.assertEqual(LBL_EQUAL, 'equal')
        self.assertEqual(LBL_INSERT, 'insert')
        self.assertEqual(LBL_REPLACE, 'replace')
