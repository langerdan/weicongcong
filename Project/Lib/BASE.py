#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : BASE_v1.00a
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : January 22 2016

import gzip
import logging
import os
import re


def read_bed(path_b):
	f_details = {}
	with open(path_b, 'rb') as r_obj_b:
		for line_b in r_obj_b:
			chr_n = re.match('([^\t]+)\t', line_b).group(1)
			pos_s = int(re.match('[^\t]+\t([^\t]+\t)', line_b).group(1))
			pos_e = int(re.match('(?:[^\t]+\t){2}([^\t]+\t)', line_b).group(1))
			gene_name = re.match('(?:[^\t]+\t){3}([^\t\n\r]+)', line_b).group(1)
			if re.search('[:\-_]', gene_name):
				gene_name = ' '
			f_details["%s-%s-%s-%s" % (chr_n, gene_name, pos_s, pos_e)] = [chr_n, gene_name, pos_s, pos_e]
	return f_details


def parse_cigar_len(operations, len_valid):
	if re.match('\d+\w', operations):
		len_frag, cigar_op = re.match('(\d+)(\w)', operations).group(1, 2)
		rest_op = operations[len(len_frag) + 1:]
		num_frag = int(len_frag)
		if cigar_op in ('M', 'I'):
			len_valid += num_frag
		elif cigar_op in ('D', 'S', 'H', 'P', 'N'):
			pass
		if rest_op:
			len_valid = parse_cigar_len(rest_op, len_valid)
	return len_valid


def get_file_path(dir_main, suffix='faa', output_type='list', r_num=2):
	def recurse_dir(dir_r, path_list, suffix_r, r_num_r):
		r_num_r -= 1
		content_list = os.listdir(dir_r)
		for each_content in content_list:
			path_content = os.path.join(dir_r, each_content)
			if os.path.isdir(path_content) and r_num_r:
				recurse_dir(path_content, path_list, suffix, r_num_r)
			elif re.search('\.' + suffix_r + '$', each_content):
				print path_content
				path_list.append(path_content)
		return path_list

	path_file = recurse_dir(dir_main, [], suffix, r_num)
	if output_type == 'list':
		return path_file
	elif output_type == 'txt':
		return '\n'.join(path_file)


def decompress_gzip(dir_main, suffix='faa', r_num=2):
	r_num -= 1
	content_list = os.listdir(dir_main)
	for each_content in content_list:
		path_content = os.path.join(dir_main, each_content)
		if os.path.isdir(path_content) and r_num:
			decompress_gzip(path_content, suffix, r_num)
		elif re.search(suffix + '\.gz$', each_content):
			path_file = os.path.join(dir_main, re.search('(.+)\.gz', each_content).group(1))
			if os.path.exists(path_file):
				pass
				# print '%s  PASS!' % path_content
			else:
				with gzip.open(path_content, 'rb') as f:
					file_obj = open(path_file, 'wb')
					file_obj.write(f.read())
					file_obj.close()
				print '%s  OK!' % path_content


def setup_logger(log_name, path_log, on_stream=False, level=logging.DEBUG,
				 format_base='%(asctime)s | %(filename)s - line:%(lineno)-4d| %(levelname)s | %(message)s',
				 format_date='%d-%b-%Y %H:%M:%S'):
	if not os.path.exists(os.path.dirname(path_log)):
		os.makedirs(os.path.dirname(path_log))
	l = logging.getLogger(log_name)
	file_handler = logging.FileHandler(path_log, mode='w')
	file_handler.setFormatter(logging.Formatter(format_base, format_date))

	l.setLevel(level)
	l.addHandler(file_handler)
	if on_stream:
		stream_handler = logging.StreamHandler()
		stream_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
		l.addHandler(stream_handler)
