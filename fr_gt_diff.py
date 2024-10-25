#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Compare config differences, skip non-essential changes
(for example: encoded passwords are differently displayed each time)
'''

import unittest
import difflib
import pprint

import lbl_df
import src_rng
import ctx_blck
import tx_place
import sngl_prd


def form_a(one_line):
    return one_line.strip().startswith('set password ENC')


def form_b(one_line):
    return one_line.strip().startswith('set psksecret ENC')


def form_c(one_line):
    return one_line.strip().startswith('set passwd ENC')


def form_d(one_line):
    return one_line.startswith('#conf_file_ver')


def form_e(one_line):
    return one_line.strip().startswith('set password2 ENC')


def form_f(one_line):
    return one_line.strip().startswith('set passphrase ENC')


def form_g(one_line):
    return one_line.strip().startswith('set store-passphrase ENC')


def form_h(one_line):
    return one_line.strip().startswith('set logon-password ENC')


def shorten(one_text, max_len):
    if max_len:
        result = one_text[:max_len]
    else:
        result = one_text
    return result


def pt(sth):
    pprint.pprint(
        list(
            map(
                lambda x: shorten(x, 0),
                sth,
                )
            )
        )


def rd(one_file):
    fd = open(one_file)
    all_lines = fd.readlines()
    fd.close()
    return all_lines


def get_matcher(fa, fb):
    seq_mtch = difflib.SequenceMatcher(None, fa, fb)
    return seq_mtch


def save_output(name_c, out_ls):
    if name_c is not None:
        all_txt = ''.join(out_ls)
        fd_out = open(name_c, 'w')
        fd_out.write(all_txt)
        print("Written %d bytes to '%s'" % (len(all_txt), name_c))
        fd_out.close()


def is_valid(*arg_ls):
    return None not in arg_ls


class InoxTool(object):
    def __init__(self):
        '''
        InoxTool:
        '''
        self.dash_bar = 78 * '-'

    def extract_sections(self):
        '''
        InoxTool:
        '''
        (
            self.ca_cert_start,
            self.ca_cert_end,
            ) = ctx_blck.dtct_blk(tx_place.sta_2_tement, tx_place.sta_1_tement, self.fa)
        (
            self.ssh_local_key_start,
            self.ssh_local_key_end,
            ) = ctx_blck.dtct_blk(tx_place.sta_3_tement, tx_place.sta_1_tement, self.fa)
        (
            self.vpn_cert_local_a_start,
            self.vpn_cert_local_a_end,
            ) = ctx_blck.dtct_blk(tx_place.sta_4_tement, tx_place.sta_1_tement, self.fa)
        (
            self.vpn_cert_local_b_start,
            self.vpn_cert_local_b_end,
            ) = ctx_blck.dtct_blk(tx_place.sta_4_tement, tx_place.sta_1_tement, self.fb)
        (
            self.vpn_cert_ca_start,
            self.vpn_cert_ca_end,
            ) = ctx_blck.dtct_blk(tx_place.sta_5_tement, tx_place.sta_1_tement, self.fa)
        (
            self.fwall_sched_one_start,
            self.fwall_sched_one_end,
            ) = ctx_blck.dtct_blk(tx_place.sta_6_tement, tx_place.sta_1_tement, self.fa)
        # self.wifi_vap_start, self.wifi_vap_end - na razie nie są używane
        (
            self.wifi_vap_start,
            self.wifi_vap_end,
            ) = ctx_blck.dtct_blk(tx_place.sta_9_tement, tx_place.sta_1_tement, self.fa)
        (
            self.sstm_snmp_start,
            self.sstm_snmp_end,
            ) = ctx_blck.dtct_blk(tx_place.sta_10_tement, tx_place.sta_1_tement, self.fa)

    def calculate_conditions(self):
        '''
        InoxTool:
        '''
        self.fwall_sched_one_start_enabled = is_valid(
            self.fwall_sched_one_start,
            self.fwall_sched_one_end,
            )
        self.sstm_snmp_enabled = is_valid(
            self.sstm_snmp_start,
            self.sstm_snmp_end,
            )
        self.vpn_cert_local_enabled = is_valid(
            self.vpn_cert_local_a_start,
            self.vpn_cert_local_a_end,
            self.vpn_cert_local_b_start,
            self.vpn_cert_local_b_end,
            )

    def take_lists(self, a_ls, b_ls):
        '''
        InoxTool:
        '''
        self.fa = a_ls
        self.fb = b_ls
        self.extract_sections()
        self.calculate_conditions()

    def show_change(self, part_a, part_b, verbose):
        '''
        InoxTool:
        '''
        if verbose:
            print(self.dash_bar)
            pt(part_a)
            pt(part_b)

    def analyze_differences(
            self,
            focus_in=None,
            ln_numbers=0,
            forced_show=0,
            name_c=None,
            display_summary=1,
            verbose=0,
            ):
        '''
        InoxTool:
        '''
        multi_replacer = sngl_prd.MultiReplacer()
        snmp_rplcr = sngl_prd.MultiReplacer(good_ls=[
            tx_place.sta_11_tement,
            tx_place.sta_12_tement,
            ])
        line_acceptor = src_rng.LineAcceptor(focus_in)
        seq_mtch = get_matcher(self.fa, self.fb)
        one_gen = seq_mtch.get_opcodes()
        delta = 0
        dlt_before = delta
        dlt_after = delta
        out_ls = []
        change_count = 0
        for change_tpl in one_gen:
            Lbl, As, Ae, Bs, Be = change_tpl
            if line_acceptor.is_ok(As):
                if ln_numbers:
                    print(change_tpl)
                part_a = self.fa[As - dlt_before:Ae + dlt_after]
                part_b = self.fb[Bs - dlt_before:Be + dlt_after]
                if forced_show:
                    if Lbl != lbl_df.LBL_EQUAL:
                        self.show_change(part_a, part_b, verbose)
                save_second = 0
                if Lbl == lbl_df.LBL_REPLACE:
                    needs_work = 1
                    if len(part_a) == 1 and len(part_b) == 1:
                        if form_a(part_a[0]) and form_a(part_b[0]):
                            needs_work = 0
                        if form_b(part_a[0]) and form_b(part_b[0]):
                            needs_work = 0
                        if form_c(part_a[0]) and form_c(part_b[0]):
                            needs_work = 0
                        if form_d(part_a[0]) and form_d(part_b[0]):
                            needs_work = 0
                        if form_e(part_a[0]) and form_e(part_b[0]):
                            needs_work = 0
                        if form_f(part_a[0]) and form_f(part_b[0]):
                            needs_work = 0
                        if form_g(part_a[0]) and form_g(part_b[0]):
                            needs_work = 0
                        if form_h(part_a[0]) and form_h(part_b[0]):
                            needs_work = 0
                    if needs_work and is_valid(self.ca_cert_start, self.ca_cert_end):
                        if self.ca_cert_start <= As <= self.ca_cert_end:
                            needs_work = 0
                    if needs_work and is_valid(self.ssh_local_key_start, self.ssh_local_key_end):
                        if self.ssh_local_key_start <= As <= self.ssh_local_key_end:
                            needs_work = 0
                    if needs_work and self.vpn_cert_local_enabled:
                        if self.vpn_cert_local_a_start <= As <= self.vpn_cert_local_a_end:
                            if self.vpn_cert_local_b_start <= Bs <= self.vpn_cert_local_b_end:
                                if self.vpn_cert_local_a_start <= Ae <= self.vpn_cert_local_a_end:
                                    if self.vpn_cert_local_b_start <= Be <= self.vpn_cert_local_b_end:
                                        needs_work = 0
                    if needs_work and is_valid(self.vpn_cert_ca_start, self.vpn_cert_ca_end):
                        if self.vpn_cert_ca_start <= As <= self.vpn_cert_ca_end:
                            needs_work = 0
                    if needs_work and self.fwall_sched_one_start_enabled:
                        if self.fwall_sched_one_start <= As <= self.fwall_sched_one_end:
                            needs_work = multi_replacer.process_replace(self.fa, self.fb, As, Ae, Bs, Be)
                    if needs_work and self.sstm_snmp_enabled:
                        if self.sstm_snmp_start <= As <= self.sstm_snmp_end:
                            needs_work = snmp_rplcr.process_replace(self.fa, self.fb, As, Ae, Bs, Be)
                    if needs_work:
                        self.show_change(part_a, part_b, verbose)
                        save_second = 1
                elif Lbl == lbl_df.LBL_INSERT:
                    save_second = 1
                elif Lbl == lbl_df.LBL_DELETE:
                    save_second = 1
                if save_second:
                    out_ls.extend(part_b)
                    change_count += 1
                else:
                    out_ls.extend(part_a)
        if display_summary:
            print('Change count: %d' % change_count)
        save_output(name_c, out_ls)


class TestDiffEngine(unittest.TestCase):
    def test_diff_engine(self):
        '''
        TestDiffEngine:
        '''
        self.assertEqual(shorten('abc', 2), 'ab')
        self.assertEqual(shorten('efgh', 1), 'e')
        self.assertEqual(shorten('efgh', 0), 'efgh')
        self.assertEqual(form_a('set password ENC'), 1)
        self.assertEqual(form_b('set psksecret ENC'), 1)
        self.assertEqual(form_c('set passwd ENC'), 1)
        self.assertEqual(form_d('#conf_file_ver'), 1)
        self.assertEqual(form_e('set password2 ENC'), 1)
        self.assertEqual(form_f('set passphrase ENC'), 1)

    def test_in_another_form(self):
        '''
        TestDiffEngine:
        '''
        obj = InoxTool()
        a_ls = [
            tx_place.sta_2_tement,
            tx_place.sta_1_tement,
            tx_place.sta_3_tement,
            tx_place.sta_1_tement,
            tx_place.sta_4_tement,
            tx_place.sta_1_tement,
            tx_place.sta_5_tement,
            tx_place.sta_1_tement,
            tx_place.sta_6_tement,
            tx_place.sta_1_tement,
            ]
        b_ls = []
        obj.take_lists(a_ls, b_ls)
        obj.analyze_differences(
            display_summary=0,
            )

    def test_both_valid(self):
        '''
        TestDiffEngine:
        '''
        self.assertEqual(is_valid(2, 3), 1)
        self.assertEqual(is_valid(None, 3), 0)
        self.assertEqual(is_valid(4, None), 0)
        self.assertEqual(is_valid(4, 5, None), 0)
