#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Generate shorter, more meaningful diff of configuration dumps
Ignore "password/certificate encryption" changes (each dump file can have different encoding)
./dixf.py --run_tests; red_green_bar.py $? $COLUMNS
'''

import sys
import unittest
import argparse

import fr_gt_diff
import lbl_df
import src_rng
import ctx_blck
import sngl_prd


FILE_A_NAME = '--old'
FILE_B_NAME = '--new'


def recognize_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(FILE_A_NAME,
                        default=None,
                        help='Previous file name')
    parser.add_argument(FILE_B_NAME,
                        default=None,
                        help='Next file name')
    parser.add_argument('--out',
                        default=None,
                        help='Output file name with simplified changes')
    parser.add_argument('--ln_numbers',
                        action='store_true', default=False,
                        help='Show line numbers with insert/replace/equal/... actions')
    parser.add_argument('--forced_show',
                        action='store_true', default=False,
                        help='Show difference lines before discarding known/ignored replacements')
    parser.add_argument('--focus_in',
                        default=None,
                        help='Focus on lines in old/previous file, for example: 4132, 4132-4162, 50- or -100')
    parser.add_argument('--run_tests',
                        action='store_true', default=False,
                        help='Run tests')
    parser.add_argument('-v', '--verbose',
                        action='store_true', default=False,
                        help='Verbose output')
    opt_bag = parser.parse_args()
    return parser, opt_bag


fast_test_ls = [
    fr_gt_diff.TestDiffEngine,
    lbl_df.TestPreparedLabels,
    src_rng.TestFocusedLines,
    ctx_blck.TestContextBlock,
    sngl_prd.TestSinglePeriod,
    ]


def add_all_fast(suite):
    for one_test in fast_test_ls:
        suite.addTest(unittest.makeSuite(one_test))


def summary_status(suite):
    text_test_result = unittest.TextTestRunner().run(suite)
    return not not (text_test_result.failures or text_test_result.errors)


def perform_slow_tests():
    suite = unittest.TestSuite()
    add_all_fast(suite)
    return summary_status(suite)


def the_main():
    result = 1
    parser, opt_bag = recognize_options()
    option_done = 0
    if opt_bag.run_tests:
        result = perform_slow_tests()
        option_done = 1
    if not option_done:
        fa = None
        fb = None
        name_a = opt_bag.old
        if name_a is not None:
            fa = fr_gt_diff.rd(name_a)
        name_b = opt_bag.new
        if name_b is not None:
            fb = fr_gt_diff.rd(name_b)
        if name_a is not None or name_b is not None:
            if name_a is None:
                parser.print_help()
                raise RuntimeError('Lacking option: %s' % FILE_A_NAME)
            if name_b is None:
                parser.print_help()
                raise RuntimeError('Lacking option: %s' % FILE_B_NAME)
            name_c = opt_bag.out
            inox_tool = fr_gt_diff.InoxTool()
            inox_tool.take_lists(fa, fb)
            inox_tool.analyze_differences(
                focus_in=opt_bag.focus_in,
                ln_numbers=opt_bag.ln_numbers,
                forced_show=opt_bag.forced_show,
                name_c=name_c,
                verbose=opt_bag.verbose,
                )
            result = 0
            option_done = 1
    if not option_done:
        parser.print_help()
    return result


if __name__ == '__main__':
    result = the_main()
    sys.exit(result)
