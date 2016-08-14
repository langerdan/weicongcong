#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : countReads_v0.01a
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : July 27 2016


from __future__ import division
import os
import re
import sys

import xlwt

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from Project.Pyject.Lib.BASE import get_file_path

# CONFIG AREA #
len_primer = 35


def read_bed(path_b):
    a_details = {}
    with open(path_b, 'rb') as r_obj_b:
        for line_b in r_obj_b:
            chr_n = re.match('([^\t]+)\t', line_b).group(1)
            pos_s = int(re.match('[^\t]+\t([^\t]+\t)', line_b).group(1))
            pos_e = int(re.match('(?:[^\t]+\t){2}([^\t]+\t)', line_b).group(1))
            gene_name = re.match('(?:[^\t]+\t){3}([^\t\n\r]+)', line_b).group(1)
            if re.search('[:\-_]', gene_name):
                gene_name = ' '
            a_details["%s-%s-%s" % (chr_n, gene_name, pos_s)] = [chr_n, pos_s, pos_e, gene_name]
    return a_details


def read_fg_list(path_fg_l):
    fg_d = {"fg_a": {}, "fg_b": {}}
    with open(path_fg_l, 'rb') as r_obj_fg:
        for line_fg in r_obj_fg:
            fg_a = re.match('([^\t]+)\t', line_fg).group(1)
            fg_b = re.match('[^\t]+\t([^\t]+)', line_fg).group(1)
            chr_n = re.match('(?:[^\t]+\t){2}([^\t]+)', line_fg).group(1)
            pos_s = int(re.match('(?:[^\t]+\t){3}([^\t]+)', line_fg).group(1))
            pos_e = int(re.match('(?:[^\t]+\t){4}([^\t\n\r]+)', line_fg).group(1))
            if fg_a not in fg_d["fg_a"]:
                fg_d["fg_a"][fg_a] = {}
                fg_d["fg_a"][fg_a]["ln-b"] = []
            fg_d["fg_a"][fg_a]["ln-b"].append("%s-%s-%s" % (fg_b, chr_n, pos_s))
            fg_d["fg_b"]["%s-%s-%s" % (fg_b, chr_n, pos_s)] = {"chr": chr_n, "pos_s": pos_s, "pos_e": pos_e}
    return fg_d


def get_fg_a_cpp(a_details, fg_d):
    for a_key in a_details:
        chr_n = a_details[a_key][0]
        gene_name = a_details[a_key][3]
        pos_s = a_details[a_key][1]
        pos_e = a_details[a_key][2]
        if gene_name in ["ALK", "FGFR3", "ROS1", "RET", "NTRK1"]:
            if gene_name not in fg_d["fg_a"]:
                fg_d["fg_a"][gene_name] = {}
            fg_d["fg_a"][gene_name]["chr"] = chr_n
            fg_d["fg_a"][gene_name]["pos_s"] = pos_s
            fg_d["fg_a"][gene_name]["pos_e"] = pos_e
    return fg_d


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


def save_tab(y_data, x_axis, tab_name):
    sum_row_list = []
    sum_col_list = [0 for x in x_axis]
    # write tab - reads
    with open(os.path.join(dir_sam, "%s-reads" % tab_name), 'wb') as w_obj:
        w_obj.write("\t%s\n" % '\t'.join(x_axis))
        for key, value in amplicon_details_sorted:
            w_obj.write(key)
            sum_row = 0
            for each_sample in y_data:
                w_obj.write("\t%d" % each_sample[key])
                sum_row += each_sample[key]
                sum_col_list[y_data.index(each_sample)] += each_sample[key]
            sum_row_list.append(sum_row)
            print "amplicon: %s sum is %d" % (key, sum_row)
            w_obj.write('\n')
        print "%d samples sum are: %s" % (len(x_axis), sum_col_list)

    # write tab - nli-sample-sum
    with open(os.path.join(dir_sam, "%s-nli-sample-sum" % tab_name), 'wb') as w_obj:
        w_obj.write("\t%s\n" % '\t'.join(x_axis))
        for key, value in amplicon_details_sorted:
            w_obj.write(key)
            for each_sample in y_data:
                sum_sample = sum_col_list[y_data.index(each_sample)]
                if sum_sample != 0:
                    w_obj.write("\t%d" % (each_sample[key] / sum_sample * 10000))
                else:
                    w_obj.write("\t0")
            w_obj.write('\n')

    # write tab - nli-amplicon-aver
    with open(os.path.join(dir_sam, "%s-nli-amplicon-aver" % tab_name), 'wb') as w_obj:
        w_obj.write("\t%s\n" % '\t'.join(x_axis))
        for key, value in amplicon_details_sorted:
            w_obj.write(key)
            for each_sample in y_data:
                aver_reads = sum_row_list[amplicon_details_sorted.index((key, value))] / len(x_axis)
                if aver_reads != 0:
                    w_obj.write("\t%d" % (each_sample[key] / aver_reads))
                else:
                    w_obj.write("\t0")
            w_obj.write('\n')


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
        print "sample: %s sum is %d" % (x, sum_col)
    print "%d amplicons sum are: %s" % (len(amplicon_details_sorted), sum_row_list)

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
    with open(os.path.join(dir_sam, log_name), 'wb') as w_obj:
        for d_key, d_value in data_sorted:
            w_obj.write("%s\t%d\n" % (d_key, d_value))
            if not re.match('@', d_key):
                mismatch_num += d_value
        w_obj.write("%s\t%d\n" % ("@Mismatch", mismatch_num))


def output_fg(data, output_name):
    data_sorted = sorted(data, key=lambda d: (d[0], d[1]))
    with open(os.path.join(dir_sam, output_name), 'wb') as w_obj:
        for each_row in data_sorted:
            w_obj.write("%s\n" % [str(x) for x in each_row].split("\t"))


if __name__ == '__main__':
    path_bed = sys.argv[1]
    dir_sam = sys.argv[2]
    path_fg_list = sys.argv[3]
    print "=>path of *.bed: %s\n=>dir of *.sam: %s=>path of fusion gene list: %s" % (path_bed, dir_sam, path_fg_list)

    print "=>get amplicon details...",
    amplicon_details = read_bed(path_bed)
    print "OK!"
    # print amplicon_details
    print "=>get fusion gene list...",
    fusion_gene_d = read_fg_list(path_fg_list)
    fusion_gene_d = get_fg_a_cpp(amplicon_details, fusion_gene_d)
    print "OK!"

    print "=>get all paths of *.sam file..."
    path_sam_list = get_file_path(dir_sam, "sam", 'list', 2)
    dir_basename = os.path.basename(dir_sam)
    print "OK! total %d." % len(path_sam_list)

    amplicon_stat = []
    sam_basename_list = []

    for each_p_sam in path_sam_list:
        print "[No.%d/%d]processing with %s..." % (path_sam_list.index(each_p_sam) + 1, len(path_sam_list), each_p_sam)
        sam_basename_list.append(re.match('([^_]+_[^_]+)', os.path.basename(each_p_sam)).group(1))
        n = None
        if re.match('BRAC', dir_basename):
            n = 35
        elif re.match('onco', dir_basename):
            n = 0
        with open(each_p_sam, 'rb') as r_obj_sam:
            counts = {}
            mismatch = {}
            fg_b_hit = {}
            fg_a_hit = {}
            fg_seq = {}
            fg_output = []
            line_i = 0
            for line_sam in r_obj_sam:
                line_i += 1
                if re.match('@', line_sam):
                    continue
                chr_name = re.match('(?:[^\t]+\t){2}([^\t]+)', line_sam).group(1)
                pos_start = int(re.match('(?:[^\t]+\t){3}([^\t]+)', line_sam).group(1))
                cigar = re.match('(?:[^\t]+\t){5}([^\t]+)', line_sam).group(1)
                len_match = parse_cigar(cigar, 0)
                pos_end = pos_start + len_match
                seq_name = re.match('([^\t]+)\t', line_sam).group(1)
                log_each = "%s-(%s-%s-%s)-%s" % (pos_start, chr_name, cigar, len_match, pos_end)
                match_trigger = 0
                for each_key in amplicon_details:
                    if each_key not in counts:
                        counts[each_key] = 0
                    if chr_name == amplicon_details[each_key][0]:
                        if pos_start >= amplicon_details[each_key][1] - n and \
                                                pos_end - 1 <= amplicon_details[each_key][2] + n:
                            counts[each_key] += 1
                            match_trigger = 1
                            break
                for gene_b_name in fusion_gene_d["fg_b"]:
                    if gene_b_name not in fg_b_hit:
                        fg_b_hit[gene_b_name] = []
                    if chr_name == fusion_gene_d["fg_b"][gene_b_name]["chr"]:
                        if pos_start >= fusion_gene_d["fg_b"][gene_b_name]["pos_s"] and \
                                                pos_end - 1 <= fusion_gene_d["fg_b"][gene_b_name]["pos_e"]:
                            fg_b_hit[gene_b_name].append(seq_name)
                            fg_seq[seq_name] = line_sam
                for fusion_gene_a in fusion_gene_d["fg_a"]:
                    if fusion_gene_a not in fg_a_hit:
                        fg_a_hit[fusion_gene_a] = []
                    if chr_name == fusion_gene_d["fg_a"][fusion_gene_a]["chr"]:
                        if pos_start >= fusion_gene_d["fg_a"][fusion_gene_a]["pos_s"] and \
                                                pos_end - 1 <= fusion_gene_d["fg_a"][fusion_gene_a]["pos_e"]:
                            fg_a_hit[fusion_gene_a].append(seq_name)
                if match_trigger == 0:
                    if log_each not in mismatch:
                        mismatch[log_each] = 1
                    else:
                        mismatch[log_each] += 1
            mismatch["@TotalReads"] = line_i
            for fusion_gene_a in fusion_gene_d["fg_a"]:
                for fusion_gene_b in fusion_gene_d["fg_a"][fusion_gene_a]["ln-b"]:
                    for seq_a in fg_a_hit[fusion_gene_a]:
                        for seq_b in fg_b_hit[fusion_gene_b]:
                            if seq_a == seq_b:
                                print "fg match: %s" % seq_b
                                gene_b_name = re.match('([^\-]+)', fusion_gene_b).group(1)
                                fg_output.append([fusion_gene_a, gene_b_name,
                                                  fusion_gene_d["fg_b"][fusion_gene_b]["chr"],
                                                  fusion_gene_d["fg_b"][fusion_gene_b]["pos_s"],
                                                  fusion_gene_d["fg_b"][fusion_gene_b]["pos_e"], fg_seq[seq_b]])
        output_mismatch(mismatch, "%s-mismatch.log" % os.path.basename(each_p_sam))
        output_fg(fg_output, "%s-fusion-gene.log" % os.path.basename(each_p_sam))
        amplicon_stat.append(counts)

    amplicon_details_sorted = sorted(amplicon_details.iteritems(), key=lambda d: (d[1][0], d[1][1]))
    print "output table...",
    save_tab(amplicon_stat, sam_basename_list, 'reads_statistics')
    save_stat(amplicon_stat, sam_basename_list)
    print "OK!\n==============================================\nDone!"


