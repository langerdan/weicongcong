#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : STdepthRegions_v0.01a
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : August 1 2016

import os
import re
import sys
import shlex
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))))
from Project.Pyject.LargeInDel.countReads_bed import read_bed

path_bed = sys.argv[1]
dir_bam = sys.argv[2]


def run_cmd(cmd, output_obj):
    args = shlex.split(cmd)
    p = subprocess.Popen(args, stdout=output_obj)
    p.wait()


def card_depth(p_depth):
    depth_amplicon = {}
    with open(p_depth, 'rb') as r_obj:
        for line in r_obj:
            chr_name = re.match('([^\t]+)\t', line).group(1)
            pos = int(re.match('[^\t]+\t([^\t]+)\t', line).group(1))
            depth = int(re.match('(:?[^\t]+\t){2}([^\t\n\r]+)', line).group(1))
            for each_key in amplicon_details:
                if chr_name == amplicon_details[each_key][0]:
                    if amplicon_details[each_key][1] <= pos <= amplicon_details[each_key][2]:
                        if each_key not in depth_amplicon:
                            depth_amplicon[each_key] = {}
                        depth_amplicon[each_key][pos] = depth
                        break
    return depth_amplicon


amplicon_details = read_bed(path_bed)
file_list = os.listdir(dir_bam)
for file_no, each_file in enumerate(file_list):
    path_each_file = os.path.join(dir_bam, each_file)
    if re.match('.+\.sort\.bam$', each_file) and os.path.isfile(path_each_file):
        print "[%d/%d]processing %s..." % (file_no + 1, len(file_list), each_file)
        path_depth = re.sub('\.sort\.bam$', '.depth.tab', path_each_file)
        with open(path_depth, 'wb') as w_obj:
            run_cmd('samtools depth -ab %s %s' % (path_bed, path_each_file), w_obj)

