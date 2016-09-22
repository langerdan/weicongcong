#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : transPrimerSheet_ver0.01a
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : July 20 2016

import os
import re
import sys

input_file = sys.argv[1]
print 'processing with %s...' % input_file
if re.match('[/~]', input_file):
	print 'perhaps you use absolute path,'
	path_input = input_file
else:
	print 'perhaps you use relative path,'
	path_input = os.path.join(os.getcwd(), input_file)


amplicon_info_file = []
with open(path_input, 'rb') as r_obj:
	for line_no, line in enumerate(r_obj):
		if line_no == 0:
			amplicon_info_file.append('AmpliconNmae\tPrimer1Sequence\tPrimer2Sequence\tAmpliconLength\tChr\t'
									  'GenomicAmpiconStart\tGenomicAmpiconEnd\n')
			continue
		amplicon_name = re.match('(?:[^\t]+\t){6}([^\t]+)', line).group(1)
		primer1seq = re.match('(?:[^\t]+\t){1}([^\t]+)', line).group(1)
		primer2seq = re.match('(?:[^\t]+\t){2}([^\t]+)', line).group(1)
		amplicon_len = re.match('(?:[^\t]+\t){10}([^\t]+)', line).group(1)
		chr_no = re.match('(?:[^\t]+\t){5}([^\t]+)', line).group(1)
		amplicon_start = re.match('(?:[^\t]+\t){6}([^\t]+)', line).group(1)
		amplicon_end = re.match('(?:[^\t]+\t){9}([^\t]+)', line).group(1)
		amplicon_info_file.append('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (amplicon_name, primer1seq, primer2seq, amplicon_len,
																    chr_no, amplicon_start, amplicon_end))

with open(os.path.join(os.getcwd(), 'amplicon_info'), 'wb') as w_obj:
	for line in amplicon_info_file:
		w_obj.write(line)
