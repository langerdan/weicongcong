#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : countReads_v0.01a
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : July 27 2016


from __future__ import division
from operator import itemgetter
import os
import re
import sys

import xlwt

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from Project.Pyject.Lib.BASE import get_file_path


def read_bed(path_b):
    amplicon_details = {}
    with open(path_b, 'rb') as r_obj_b:
        for line_no, line_b in enumerate(r_obj_b):
            if line_no >= 3:
                chr_n = re.match('([^\t]+)\t', line_b).group(1)
                pos_s = int(re.match('[^\t]+\t([^\t]+\t)', line_b).group(1))
                pos_e = int(re.match('(?:[^\t]+\t){2}([^\t]+\t)', line_b).group(1))
                gene_name = re.match('(?:[^\t]+\t){3}([^\t\n\r]+)', line_b).group(1)
                if re.match('[:-]', gene_name):
                    gene_name = ' '
                amplicon_details["%s-%s-%s" % (chr_n, gene_name, pos_s)] = [chr_n, pos_s, pos_e]
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


def save_tab(x_data, y_axis, tab_name):
    with open(os.path.join(dir_sam, tab_name), 'wb') as w_obj:
        w_obj.write("\t%s\n" % '\t'.join(y_axis))
        for each_sample in x_data:
            w_obj.write(each_sample)
            for key in a_details_sorted:
                w_obj.write("\t%s" % each_sample[key])
            w_obj.write('\n')


def save_stat(x_data, y_axis):
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

    sum_row_list = []
    sum_col_list = [0 for x in a_details_sorted]
    # write sheet 1
    for (row_no, row_data) in enumerate(x_data):
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
    for (row_no, row_data) in enumerate(x_data):
        sheet2.write(row_no + 1, 0, y_axis[row_no], set_style(220, True))
        for (key, value) in a_details_sorted:
            sheet2.write(0, a_details_sorted.index((key, value)) + 1, key, set_style(220, True))
            sheet2.write(row_no + 1, a_details_sorted.index((key, value)) + 1,
                         row_data[key] / sum_row_list[a_details_sorted.index((key, value))] * 10000)

    # write_sheet 3
    for (row_no, row_data) in enumerate(x_data):
        sheet3.write(row_no + 1, 0, y_axis[row_no], set_style(220, True))
        for (key, value) in a_details_sorted:
            sheet3.write(0, a_details_sorted.index((key, value)) + 1, key, set_style(220, True))
            sheet3.write(row_no + 1, a_details_sorted.index((key, value)) + 1,
                         row_data[key] / sum_col_list[a_details_sorted.index((key, value))] * len(a_details_sorted))

    workbook.save(path_xls)


path_bed = sys.argv[1]
dir_sam = sys.argv[2]
print "=>path of *.bed: %s\n=>dir of *.sam: %s" % (path_bed, dir_sam)

print "=>get amplicon details...",
a_details = read_bed(path_bed)
print "OK!"
print a_details
amplicon_stat = []

print "=>get all paths of *.sam file...",
path_sam_list = get_file_path(dir_sam, "sam")
print "OK! total %d." % len(path_sam_list)

sam_basename_list = []
for each_p_sam in path_sam_list:
    print "processing with %s..." % each_p_sam
    sam_basename_list.append(re.match('(.+)\.sam', os.path.basename(each_p_sam)).group(1))
    with open(each_p_sam, 'rb') as r_obj_sam:
        counts = {}
        for line_sam in r_obj_sam:
            if re.match('@', line_sam):
                continue
            chr_name = re.match('(?:[^\t]+\t){2}([^\t]+)', line_sam).group(1)
            pos_start = int(re.match('(?:[^\t]+\t){3}([^\t]+)', line_sam).group(1))
            cigar = re.match('(?:[^\t]+\t){5}([^\t]+)', line_sam).group(1)
            len_match = parse_cigar(cigar, 0)
            pos_end = pos_start + len_match
            if len_match == 0:
                print "0 warning: %s - %s = %s - %s" % (pos_start, cigar, len_match, pos_end)
            for each_key in a_details:
                if each_key not in counts:
                    counts[each_key] = 0
                if chr_name == a_details[each_key][0]:
                    if pos_start >= a_details[each_key][1] and pos_end <= a_details[each_key][2]:
                        counts[each_key] += 1
    amplicon_stat.append(counts)

a_details_sorted = sorted(a_details.iteritems(), key=itemgetter(0, 1))
print "output table...",
save_tab(amplicon_stat, sam_basename_list, 'reads_statistics.txt')
save_stat(amplicon_stat, sam_basename_list)
print "OK!\n==============================================\nDone!"


