#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : countReads_v0.01a
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : July 21 2016

import os
import re
import sys
import xlwt
from Pyject.Lib.BASE import get_file_path


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
            #print "%s - %s" % (amplicon_name, [amplicon_start, amplicon_end, insert_start, insert_end])
    return amplicon_details


def save_stat(y_data1, y_data2, x_axis):
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
    sheet2 = workbook.add_sheet(u'insert', cell_overwrite_ok=True)
    a_details_sorted = sorted(a_details.iteritems(), key=lambda d: d[0])
    for (row_no, row_data) in enumerate(y_data1):
        sheet1.write(row_no + 1, 0, x_axis[row_no], set_style(220, True))
        for (key, value) in a_details_sorted:
            sheet1.write(0, a_details_sorted.index((key, value)) + 1, key, set_style(220, True))
            sheet1.write(row_no + 1, a_details_sorted.index((key, value)) + 1, row_data[key])
    for (row_no, row_data) in enumerate(y_data2):
        sheet2.write(row_no + 1, 0, x_axis[row_no], set_style(220, True))
        for (key, value) in a_details_sorted:
            sheet2.write(0, a_details_sorted.index((key, value)) + 1, key, set_style(220, True))
            sheet2.write(row_no + 1, a_details_sorted.index((key, value)) + 1, row_data[key])
    workbook.save(path_xls)


path_primer_details = sys.argv[1]
dir_sam = sys.argv[2]
print '=>path of primer_details: %s\n=>dir of *.sam: %s' % (path_primer_details, dir_sam)

print '=>get amplicon details...',
a_details = read_primer_details(path_primer_details)
print 'OK!'
print a_details
amplicon_stat_am = []
amplicon_stat_in = []

print '=>get all paths of *.sam file...'
path_sam_list = get_file_path(dir_sam, 'sam')
print 'OK! total %d.' % len(path_sam_list)

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
            m_pos = int(re.match('(?:[^\t]+\t){7}([^\t]+)', line).group(1))
            for each_key in a_details:
                if each_key not in counts_am:
                    counts_am[each_key] = 0
                if pos_start >= a_details[each_key][0] and m_pos <= a_details[each_key][1]:
                    counts_am[each_key] += 1
                if each_key not in counts_in:
                    counts_in[each_key] = 0
                if pos_start >= a_details[each_key][2] and m_pos <= a_details[each_key][3]:
                    counts_in[each_key] += 1
        #print "count_am: %s" % counts_am
    amplicon_stat_am.append(counts_am)
    amplicon_stat_in.append(counts_in)

save_stat(amplicon_stat_am, amplicon_stat_in, sam_basename_list)
