#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : countReads_via_depth
# AUTHOR  : codeunsolved@gmail.com
# CREATED : November 6 2016
# VERSION : v0.0.1a

from __future__ import division
import os
import re
import sys
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Project.Lib.BASE import read_bed
from Project.Lib.BASE import print_colors
from Project.Lib.BASE import get_file_path

# CONFIG AREA #
dir_depth = sys.argv[1]
path_bed = sys.argv[2]


def save_tab(y_data, x_axis, tab_name):
    with open(os.path.join(dir_depth, tab_name), 'wb') as tab:
        tab.write('\t%s\n' % '\t'.join(x_axis))
        for key, value in amplicon_details_sorted:
            tab.write(key)
            for sample in y_data:
                tab.write("\t%s" % sample[key])
            tab.write('\n')


def init_amplicon_data(sap_name):
    def init_amplicon_cover():
        amplicon_cover = {}
        for f_key in amplicon_details:
            amplicon_cover[f_key] = {"amp_name": f_key,
                                     "chr_num": re.match('chr(.+)', amplicon_details[f_key][0]).group(1),
                                     "gene_name": amplicon_details[f_key][1],
                                     "pos_s": amplicon_details[f_key][2], "pos_e": amplicon_details[f_key][3],
                                     "len": amplicon_details[f_key][3] - amplicon_details[f_key][2] + 1,
                                     "x_labels": [], "depths": [],
                                     "reads": None
                                     }
        return amplicon_cover

    amplicon_data = {"sample_name": sap_name,
                     "amp_cover": init_amplicon_cover(),
                     "data_ver": "v0.0.1"
                     }
    return amplicon_data


def get_reads(data):
    n = 0
    while True:
        pop_i = []
        for i, d in enumerate(data['depths']):
            if d == n:
                pop_i.append(i)
        for p_i in sorted(list(set(pop_i)), reverse=True):
            data['depths'].pop(p_i)
        if len(data['depths']) < data['len'] * 0.7:
            # print "[%s] %s" % (data['amp_name'], n)
            return n
        n += 1

if __name__ == '__main__':
    print "========================================================"
    print datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    print "========================================================"
    print print_colors("=> path of *.bed: %s\n=> dir of *.depth: %s" % (path_bed, dir_depth), 'yellow')

    print print_colors("• get amplicon details..."),
    amplicon_details = read_bed(path_bed)
    amplicon_details_sorted = sorted(amplicon_details.iteritems(), key=lambda d: (d[1][0], d[1][2]))
    print print_colors("OK!", 'green')
    # print amplicon_details

    print print_colors("• get all paths of *.depth file...")
    path_depth_list = get_file_path(dir_depth, "depth", 'list', 1, False)
    dir_basename = os.path.basename(dir_depth)
    print print_colors("OK! total %d." % len(path_depth_list), 'green')
    print "========================================================"

    sample_reads_list = []
    sample_name_list = []
    for p_depth in path_depth_list:
        sample_reads = {}
        print print_colors("<No.%d/%d %s>" % (path_depth_list.index(p_depth) + 1, len(path_depth_list), p_depth))
        file_name = re.match('(.+)\.depth', os.path.basename(p_depth)).group(1)
        if re.search('_S\d+', file_name):
            sample_name = re.match('(.+)_S\d+', file_name).group(1)

        sample_name_list.append(sample_name)
        with open(p_depth, 'rb') as depth:
            amp_data = init_amplicon_data(sample_name)
            for i, line_depth in enumerate(depth):
                chr_n = re.match('([^\t]+)\t', line_depth).group(1)
                pos = int(re.match('[^\t]+\t([^\t]+\t)', line_depth).group(1))
                depth = int(re.match('(?:[^\t]+\t){2}([^\t\r\n]+)', line_depth).group(1))
                for key, value in amplicon_details_sorted:
                    if chr_n == value[0] and value[2] <= pos <= value[3]:
                        amp_data['amp_cover'][key]['x_labels'].append(pos)
                        amp_data['amp_cover'][key]['depths'].append(depth)

            for key in amp_data['amp_cover']:
                if len(amp_data['amp_cover'][key]['x_labels']) != 0:
                    amp_data['amp_cover'][key]['reads'] = get_reads(amp_data['amp_cover'][key])
                else:
                    # add absent amplicon
                    amp_data['amp_cover'][key]['reads'] = 0
                sample_reads[key] = amp_data['amp_cover'][key]['reads']

    sample_reads_list.append(sample_reads)

    print print_colors("• output table ..."),
    save_tab(sample_reads_list, sample_name_list, 'reads_counts')
    print print_colors("OK!", 'green')
