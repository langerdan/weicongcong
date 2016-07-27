#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : countReads_v0.01a
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : July 21 2016

from __future__ import division
import os
import re
import sys

import xlwt

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from Project.Pyject.Lib.BASE import get_file_path


def read_primer_details(p_file):
    amplicon_details = {}
    with open(p_file, 'rb') as r_obj_p:
        for (line_no, line_co) in enumerate(r_obj_p):
            if line_no == 0 or line_no == 1:
                continue
            amplicon_name = re.match('(?:[^\t]+\t){11}([^\t]+)', line_co).group(1)
            # fwd_primer = re.match('(?:[^\t]+\t){1}([^\t]+)', line).group(1)
            # rev_primer = re.match('(?:[^\t]+\t){2}([^\t]+)', line).group(1)
            # chr_name = re.match('(?:[^\t]+\t){5}([^\t]+)', line).group(1)
            # amplicon_len = re.match('(?:[^\t]+\t){10}([^\t]+)', line).group(1)
            insert_start = int(re.match('(?:[^\t]+\t){7}([^\t]+)', line_co).group(1))
            insert_end = int(re.match('(?:[^\t]+\t){8}([^\t]+)', line_co).group(1))
            amplicon_start = int(re.match('(?:[^\t]+\t){6}([^\t]+)', line_co).group(1))
            amplicon_end = int(re.match('(?:[^\t]+\t){9}([^\t]+)', line_co).group(1))
            amplicon_details[amplicon_name] = [amplicon_start, amplicon_end, insert_start, insert_end]
            # print "%s - %s" % (amplicon_name, [amplicon_start, amplicon_end, insert_start, insert_end])
    return amplicon_details


def parse_cigar(operations, len_valid):
    # print operations
    if re.match('\d+\w', operations):
        len_frag, cigar_op = re.match('(\d+)(\w)', operations).group(1, 2)
        rest_op = operations[len(len_frag) + 1:]
        len_frag = int(len_frag)
        if cigar_op in ('M', 'I'):
            len_valid += len_frag
        elif cigar_op in ('D', 'S', 'H', 'P', 'N'):
            pass
        if rest_op:
            len_valid = parse_cigar(rest_op, len_valid)
    return len_valid


def save_temp(x_data, y_axis, tab_name):
    pass


def save_stat(x_data1, x_data2, y_axis):
    def set_style(height=210, bold=False, color_index=xlwt.Style.colour_map['black'], name='Microsoft YaHei UI'):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.colour_index = color_index
        font.height = height
        style.font = font
        return style

    path_xls = os.path.join(dir_sam, 'reads_stat.xls')
    workbook = xlwt.Workbook(style_compression=2)

    sheet1 = workbook.add_sheet(u'amplicon', cell_overwrite_ok=True)
    sheet2 = workbook.add_sheet(u'normal-sample', cell_overwrite_ok=True)
    sheet3 = workbook.add_sheet(u'normal-aver', cell_overwrite_ok=True)
    sheet4 = workbook.add_sheet(u'insert', cell_overwrite_ok=True)

    sum_row_list = []
    sum_col_list = [0 for x in a_details_sorted]
    # write sheet 1
    for (row_no, row_data) in enumerate(x_data1):
        sheet1.write(row_no + 1, 0, y_axis[row_no], set_style(220, True))
        sum_row = 0
        for (key, value) in a_details_sorted:
            sheet1.write(0, a_details_sorted.index((key, value)) + 1, key, set_style(220, True))
            sheet1.write(row_no + 1, a_details_sorted.index((key, value)) + 1, row_data[key])
            sum_row += row_data[key]
            sum_col_list[a_details_sorted.index((key, value))] += row_data[key]
        sum_row_list.append(sum_row)
        print "sample: %s sum is %d" % (y_axis[row_no], sum_row)
        print "%d cols sum are: %s" % (len(a_details_sorted), sum_col_list)

    # write sheet 2
    for (row_no, row_data) in enumerate(x_data1):
        sheet2.write(row_no + 1, 0, y_axis[row_no], set_style(220, True))
        for (key, value) in a_details_sorted:
            sheet2.write(0, a_details_sorted.index((key, value)) + 1, key, set_style(220, True))
            sheet2.write(row_no + 1, a_details_sorted.index((key, value)) + 1,
                         row_data[key] / sum_row_list[a_details_sorted.index((key, value))] * 10000)

    # write_sheet 3
    for (row_no, row_data) in enumerate(x_data1):
        sheet3.write(row_no + 1, 0, y_axis[row_no], set_style(220, True))
        for (key, value) in a_details_sorted:
            sheet3.write(0, a_details_sorted.index((key, value)) + 1, key, set_style(220, True))
            sheet3.write(row_no + 1, a_details_sorted.index((key, value)) + 1,
                         row_data[key] / sum_col_list[a_details_sorted.index((key, value))] * len(a_details_sorted))

    # write sheet 4
    for (row_no, row_data) in enumerate(x_data2):
        sheet4.write(row_no + 1, 0, y_axis[row_no], set_style(220, True))
        for (key, value) in a_details_sorted:
            sheet4.write(0, a_details_sorted.index((key, value)) + 1, key, set_style(220, True))
            sheet4.write(row_no + 1, a_details_sorted.index((key, value)) + 1, row_data[key])

    workbook.save(path_xls)


path_primer_details = sys.argv[1]
dir_sam = sys.argv[2]
print "=>path of primer_details: %s\n=>dir of *.sam: %s" % (path_primer_details, dir_sam)

print "=>get amplicon details...",
a_details = read_primer_details(path_primer_details)
print "OK!"
print a_details
amplicon_stat_am = []
amplicon_stat_in = []

print "=>get all paths of *.sam file...",
path_sam_list = get_file_path(dir_sam, "sam")
print "OK! total %d." % len(path_sam_list)

sam_basename_list = []
for each_p_sam in path_sam_list:
    print "processing with %s..." % each_p_sam
    sam_basename_list.append(re.match('(.+)\.sam', os.path.basename(each_p_sam)).group(1))
    with open(each_p_sam, 'rb') as r_obj:
        counts_am = {}
        counts_in = {}
        for line in r_obj:
            if re.match('@', line):
                continue
            pos_start = int(re.match('(?:[^\t]+\t){3}([^\t]+)', line).group(1))
            cigar = re.match('(?:[^\t]+\t){5}([^\t]+)', line).group(1)
            len_match = parse_cigar(cigar, 0)
            pos_end = pos_start + len_match
            if len_match == 0:
                print "0 warning: %s - %s = %s - %s" % (pos_start, cigar, len_match, pos_end)
            for each_key in a_details:
                if each_key not in counts_am:
                    counts_am[each_key] = 0
                if pos_start >= a_details[each_key][0] and pos_end <= a_details[each_key][1]:
                    counts_am[each_key] += 1
                if each_key not in counts_in:
                    counts_in[each_key] = 0
                if pos_start >= a_details[each_key][2] and pos_end <= a_details[each_key][3]:
                    counts_in[each_key] += 1
                    # print "count_am: %s" % counts_am
    amplicon_stat_am.append(counts_am)
    amplicon_stat_in.append(counts_in)

a_details_sorted = sorted(a_details.iteritems(), key=lambda d: d[0])
print "output table...",
save_stat(amplicon_stat_am, amplicon_stat_in, sam_basename_list)
print "OK!\n==============================================\nDone!"