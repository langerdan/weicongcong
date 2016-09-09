#!/use/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : countReads_v0.01
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : July 27 2016
# UPDATE   : [v0.01] September 2 2016
# 1. add reduplicate statistics


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
            gene_name = re.match('(?:[^\t]+\t){3}([^\t\r\n]+)', line_b).group(1)
            if re.search('[:-_]', gene_name):
                gene_name = ' '
            a_details["%s-%s-%s" % (chr_n, gene_name, pos_s)] = [chr_n, pos_s, pos_e, gene_name]
    return a_details


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


def read_fg_list(path_fg_l):
    fg_d = {"fg_a": {}, "fg_b": {}, "ln_b": {}}
    with open(path_fg_l, 'rb') as r_obj_fg:
        for line_fg in r_obj_fg:
            fg_a = re.match('([^\t]+)\t', line_fg).group(1)
            fg_b = re.match('[^\t]+\t([^\t]+)', line_fg).group(1)
            chr_n = re.match('(?:[^\t]+\t){2}([^\t]+)', line_fg).group(1)
            pos_s = int(re.match('(?:[^\t]+\t){3}([^\t]+)', line_fg).group(1))
            pos_e = int(re.match('(?:[^\t]+\t){4}([^\t\r\n]+)', line_fg).group(1))
            if fg_a not in fg_d["ln_b"]:
                fg_d["ln_b"][fg_a] = []
            fg_d["ln_b"][fg_a].append("%s-%s-%s" % (fg_b, chr_n, pos_s))
            fg_d["fg_b"]["%s-%s-%s" % (fg_b, chr_n, pos_s)] = {"chr": chr_n, "pos_s": pos_s, "pos_e": pos_e}
    return fg_d


def get_fg_a_cpp(a_details, fg_d):
    for a_key in a_details:
        chr_n = a_details[a_key][0]
        gene_name = a_details[a_key][3]
        pos_s = a_details[a_key][1]
        pos_e = a_details[a_key][2]
        if gene_name in ["ALK", "FGFR3", "ROS1", "RET", "NTRK1"]:
            gene_a_key = "%s-%s-%s" % (gene_name, chr_n, pos_s)
            if gene_a_key not in fg_d["fg_a"]:
                fg_d["fg_a"][gene_a_key] = {}
            fg_d["fg_a"][gene_a_key]["chr"] = chr_n
            fg_d["fg_a"][gene_a_key]["pos_s"] = pos_s
            fg_d["fg_a"][gene_a_key]["pos_e"] = pos_e
    return fg_d


def output_fg(data, dedup_stat, output_name):
    data_sorted = sorted(data, key=lambda d: (d[0], d[1]))
    with open(os.path.join(dir_sam, output_name), 'wb') as w_obj:
        for each_row in data_sorted:
            w_obj.write("%s" % "\t".join([str(x) for x in each_row]))
        w_obj.write("==\tdeDup stat:\t==\n")
        for each_key in dedup_stat:
            w_obj.write("%s\t%d\n" % (each_key, dedup_stat[each_key][0]))
            print "deDup stat: %s - %d" % (each_key, dedup_stat[each_key][0])


if __name__ == '__main__':
    path_bed = sys.argv[1]
    dir_sam = sys.argv[2]
    path_fg_list = sys.argv[3]
    print "=>path of *.bed: %s\n=>dir of *.sam: %s\n=>path of fusion gene list: %s" % (path_bed, dir_sam, path_fg_list)

    print "=>get amplicon details...",
    amplicon_details = read_bed(path_bed)
    print "OK!"
    # print amplicon_details

    print "=>get fusion gene list...",
    fg_details = read_fg_list(path_fg_list)
    fg_details = get_fg_a_cpp(amplicon_details, fg_details)
    print "OK!"

    print "=>get all paths of *.sam file..."
    path_sam_list = get_file_path(dir_sam, "sam", 'list', 2)
    dir_basename = os.path.basename(dir_sam)
    print "OK! total %d." % len(path_sam_list)

    for each_p_sam in path_sam_list:
        print "[No.%d/%d]processing with %s..." % (path_sam_list.index(each_p_sam) + 1, len(path_sam_list), each_p_sam)
        n = None
        if re.match('BRCA', dir_basename):
            n = len_primer
        elif re.match('onco|56gene|lung', dir_basename):
            n = 0
        with open(each_p_sam, 'rb') as r_obj_sam:
            fg_a_hit = {}
            fg_b_hit = {}
            fg_seq = {}
            fg_output = []
            fg_dedup = {}
            line_i = 0
            for line_sam in r_obj_sam:
                line_i += 1
                if re.match('@', line_sam):
                    continue
                chr_name = re.match('(?:[^\t]+\t){2}([^\t]+)', line_sam).group(1)
                pos_start = int(re.match('(?:[^\t]+\t){3}([^\t]+)', line_sam).group(1))
                cigar = re.match('(?:[^\t]+\t){5}([^\t]+)', line_sam).group(1)
                len_match = parse_cigar(cigar, 0)
                pos_end = pos_start + len_match - 1
                seq_name = re.match('([^\t]+)\t', line_sam).group(1)
                seq = re.match('(?:[^\t]+\t){9}([^\t]+)', line_sam).group(1)
                for fusion_gene_b in fg_details["fg_b"]:
                    if chr_name == fg_details["fg_b"][fusion_gene_b]["chr"]:
                        if fg_details["fg_b"][fusion_gene_b]["pos_s"] <= pos_start <= \
                                fg_details["fg_b"][fusion_gene_b]["pos_e"] or \
                                fg_details["fg_b"][fusion_gene_b]["pos_s"] <= pos_end <= \
                                fg_details["fg_b"][fusion_gene_b]["pos_e"]:
                            if fusion_gene_b not in fg_b_hit:
                                fg_b_hit[fusion_gene_b] = {}
                            fg_b_hit[fusion_gene_b][seq_name] = 1
                            if seq_name not in fg_seq:
                                fg_seq[seq_name] = line_sam
                            elif len(seq) > (fg_seq[seq_name]):
                                fg_seq[seq_name] = line_sam
                            break
                for fusion_gene_a in fg_details["fg_a"]:
                    if chr_name == fg_details["fg_a"][fusion_gene_a]["chr"]:
                        if fg_details["fg_a"][fusion_gene_a]["pos_s"] <= pos_start <= \
                                fg_details["fg_a"][fusion_gene_a]["pos_e"] or \
                                fg_details["fg_a"][fusion_gene_a]["pos_s"] <= pos_end <= \
                                fg_details["fg_a"][fusion_gene_a]["pos_e"]:
                            if fusion_gene_a not in fg_a_hit:
                                fg_a_hit[fusion_gene_a] = {}
                            fg_a_hit[fusion_gene_a][seq_name] = 1
                            if seq_name not in fg_seq:
                                fg_seq[seq_name] = line_sam
                            elif len(seq) > (fg_seq[seq_name]):
                                fg_seq[seq_name] = line_sam
                            break

            for fg_a in fg_a_hit:
                for fg_a_sn in fg_a_hit[fg_a]:
                    gene_a_name = re.match('([^-]+)\-', fg_a).group(1)
                    for fg_b in fg_details["ln_b"][gene_a_name]:
                        if fg_b in fg_b_hit:
                            for fg_b_sn in fg_b_hit[fg_b]:
                                if fg_a_sn == fg_b_sn:
                                    fg_output.append([gene_a_name, re.match('([^-]+)\-', fg_b).group(1),
                                        fg_details["fg_b"][fg_b]["chr"],
                                        fg_details["fg_b"][fg_b]["pos_s"], fg_details["fg_b"][fg_b]["pos_e"],
                                        fg_seq[fg_a_sn]])
                                    key_name = "%s-%s-%s-%s" % (gene_a_name, re.match('([^-]+)\-', fg_b).group(1),
                                        fg_details["fg_b"][fg_b]["chr"], fg_details["fg_b"][fg_b]["pos_s"])
                                    if key_name not in fg_dedup:
                                        fg_dedup[key_name] = [1, fg_seq[fg_a_sn]]
                                    if fg_seq[fg_a_sn] not in fg_dedup[key_name]:
                                        fg_dedup[key_name].append(fg_seq[fg_a_sn])
                                        fg_dedup[key_name][0] += 1
                                    print "got fusion gene: %s, (%s - %s)" % (fg_a_sn, fg_a, fg_b)

        print "output fusion-gene log..."
        output_filename = "%s-fusion-gene.log" % re.match('(.+)\.sam', os.path.basename(each_p_sam)).group(1)
        if fg_output:
            output_fg(fg_output, fg_dedup, output_filename)
        else:
            open(os.path.join(dir_sam, output_filename, 'wb'))
        print "OK!"

    print "==============================================\nDone!"
