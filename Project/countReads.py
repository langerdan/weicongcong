#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : countReads
# AUTHOR  : codeunsolved@gmail.com
# CREATED : July 27 2016
# VERSION : v0.0.1
# UPDATE  : [v0.0.1] September 6 2016
# 1. revise BRCA pos_s and pos_e by adding len_primer; 2. revise table name; 3. add mismatch log

from __future__ import division
import os
import re
import sys
import datetime

import xlwt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Project.Lib.BASE import read_bed
from Project.Lib.BASE import print_colors
from Project.Lib.BASE import get_file_path
from Project.Lib.BASE import parse_cigar_len

# CONFIG AREA #
dir_sam = sys.argv[1]
path_bed = sys.argv[2]
len_primer = 35


def save_tab(y_data, x_axis, tab_name):
    sum_row_list = []
    sum_col_list = [0 for x in x_axis]
    # write tab - reads
    with open(os.path.join(dir_sam, "%s-reads" % tab_name), 'wb') as reads:
        reads.write("\t%s\n" % '\t'.join(x_axis))
        for key, value in amplicon_details_sorted:
            reads.write(key)
            sum_row = 0
            for sample in y_data:
                reads.write("\t%d" % sample[key])
                sum_row += sample[key]
                sum_col_list[y_data.index(sample)] += sample[key]
            sum_row_list.append(sum_row)
            # print "amplicon: %s sum is %d" % (key, sum_row)
            reads.write('\n')
        # print "%d samples sum are: %s" % (len(x_axis), sum_col_list)

    # write tab - nli-sample-sum
    with open(os.path.join(dir_sam, "%s-nli-sample-sum" % tab_name), 'wb') as nli_ss:
        nli_ss.write("\t%s\n" % '\t'.join(x_axis))
        for key, value in amplicon_details_sorted:
            nli_ss.write(key)
            for sample in y_data:
                sum_sample = sum_col_list[y_data.index(sample)]
                if sum_sample != 0:
                    nli_ss.write("\t%d" % (sample[key] / sum_sample * 10000))
                else:
                    nli_ss.write("\t0")
            nli_ss.write('\n')

    # write tab - nli-amplicon-aver
    with open(os.path.join(dir_sam, "%s-nli-amplicon-aver" % tab_name), 'wb') as nli_aa:
        nli_aa.write("\t%s\n" % '\t'.join(x_axis))
        for key, value in amplicon_details_sorted:
            nli_aa.write(key)
            for sample in y_data:
                aver_reads = sum_row_list[amplicon_details_sorted.index((key, value))] / len(x_axis)
                if aver_reads != 0:
                    nli_aa.write("\t%d" % (sample[key] / aver_reads))
                else:
                    nli_aa.write("\t0")
            nli_aa.write('\n')


def save_stat(y_data, x_axis):
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

    sheet1 = workbook.add_sheet(u'reads', cell_overwrite_ok=True)
    sheet2 = workbook.add_sheet(u'nli-sample-sum', cell_overwrite_ok=True)
    sheet3 = workbook.add_sheet(u'nli-amplicon-aver', cell_overwrite_ok=True)

    sum_row_list = [0 for x in amplicon_details_sorted]
    sum_col_list = []
    # write sheet1 - reads
    for key, value in amplicon_details_sorted:
        sheet1.write(amplicon_details_sorted.index((key, value)) + 1, 0, key, set_style(220, True))
    for x_no, x in enumerate(x_axis):
        sheet1.write(0, x_no + 1, x, set_style(220, True))
        sum_col = 0
        for key, value in amplicon_details_sorted:
            sheet1.write(amplicon_details_sorted.index((key, value)) + 1, x_no + 1, y_data[x_no][key])
            sum_col += y_data[x_no][key]
            sum_row_list[amplicon_details_sorted.index((key, value))] += y_data[x_no][key]
        sum_col_list.append(sum_col)
        #print "sample: %s sum is %d" % (x, sum_col)
    #print "%d amplicons sum are: %s" % (len(amplicon_details_sorted), sum_row_list)

    # write sheet2 - nli-sample-sum
    for key, value in amplicon_details_sorted:
        sheet2.write(amplicon_details_sorted.index((key, value)) + 1, 0, key, set_style(220, True))
    for x_no, x in enumerate(x_axis):
        sheet2.write(0, x_no + 1, x, set_style(220, True))
        sample_sum = sum_col_list[x_no]
        for key, value in amplicon_details_sorted:
            if sample_sum != 0:
                sheet2.write(amplicon_details_sorted.index((key, value)) + 1, x_no + 1, y_data[x_no][key] / sample_sum * 10000)
            else:
                sheet2.write(amplicon_details_sorted.index((key, value)) + 1, x_no + 1, 0)

    # write_sheet3 - nli-amplicon-aver
    for x_no, x in enumerate(x_axis):
        sheet3.write(0, x_no + 1, x, set_style(220, True))
    for key, value in amplicon_details_sorted:
        for x_no, x in enumerate(x_axis):
            sheet3.write(amplicon_details_sorted.index((key, value)) + 1, 0, key, set_style(220, True))
            amplicon_aver = sum_row_list[amplicon_details_sorted.index((key, value))] / len(x_axis)
            if amplicon_aver != 0:
                sheet3.write(amplicon_details_sorted.index((key, value)) + 1, x_no + 1, y_data[x_no][key] / amplicon_aver)
            else:
                sheet3.write(amplicon_details_sorted.index((key, value)) + 1, x_no + 1, 0)

    workbook.save(path_xls)


def output_mismatch(data, log_name):
    data_sorted = sorted(data.iteritems(), key=lambda d: d[0])
    mismatch_num = 0
    with open(os.path.join(dir_sam, log_name), 'wb') as mismatch:
        for d_key, d_value in data_sorted:
            mismatch.write("%s\t%d\n" % (d_key, d_value))
            if not re.match('@', d_key):
                mismatch_num += d_value
        mismatch.write("%s\t%d\n" % ("@Mismatch", mismatch_num))


if __name__ == '__main__':
    print "========================================================"
    print datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    print "========================================================"
    print print_colors("=> path of *.bed: %s\n=>dir of *.sam: %s" % (path_bed, dir_sam), 'yellow')

    print print_colors("• get amplicon details..."),
    amplicon_details = read_bed(path_bed)
    print print_colors("OK!", 'green')
    # print amplicon_details

    print print_colors("• get all paths of *.sam file...")
    path_sam_list = get_file_path(dir_sam, "sam", 'list', 1, False)
    dir_basename = os.path.basename(dir_sam)
    print print_colors("OK! total %d." % len(path_sam_list), 'green')
    print "========================================================"

    amplicon_stat = []
    sam_basename_list = []
    for p_sam in path_sam_list:
        print print_colors("<No.%d/%d %s>" % (path_sam_list.index(p_sam) + 1, len(path_sam_list), p_sam))
        sam_basename = re.match('(.+)\.sam', os.path.basename(p_sam)).group(1)
        if re.search('_S\d+', sam_basename):
            sam_basename = re.match('(.+)_S\d+', sam_basename).group(1)
        sam_basename_list.append(sam_basename)
        n = 35 if re.match('BRCA', dir_basename) else 0
        with open(p_sam, 'rb') as sam:
            counts = {}
            mismatch = {}
            for i, line_sam in enumerate(sam):
                if re.match('@', line_sam):
                    continue
                chr_name = re.match('(?:[^\t]+\t){2}([^\t]+)', line_sam).group(1)
                pos_start = int(re.match('(?:[^\t]+\t){3}([^\t]+)', line_sam).group(1))
                cigar = re.match('(?:[^\t]+\t){5}([^\t]+)', line_sam).group(1)
                len_match = parse_cigar_len(cigar, 0)
                pos_end = pos_start + len_match - 1
                match_trigger = 0
                for key in amplicon_details:
                    if key not in counts:
                        counts[key] = 0
                    if chr_name == amplicon_details[key][0]:
                        if pos_start >= amplicon_details[key][2] - n and pos_end <= amplicon_details[key][3] + n:
                            counts[key] += 1
                            match_trigger = 1
                            break
                # log mismatch
                log_mis = "%s-(%s-%s-%s)-%s" % (pos_start, chr_name, cigar, len_match, pos_end)
                if match_trigger == 0:
                    if log_mis not in mismatch:
                        mismatch[log_mis] = 1
                    else:
                        mismatch[log_mis] += 1
            mismatch["@TotalReads"] = i
            output_mismatch(mismatch, "%s-mismatch.log" % re.match('(.+)\.sam', os.path.basename(p_sam)).group(1))
        amplicon_stat.append(counts)

    amplicon_details_sorted = sorted(amplicon_details.iteritems(), key=lambda d: (d[1][0], d[1][1]))
    print print_colors("• output table ..."),
    save_tab(amplicon_stat, sam_basename_list, 'reads_statistics')
    save_stat(amplicon_stat, sam_basename_list)
    print print_colors("OK!", 'green')
