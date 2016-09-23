#!/use/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : markFusionGene
# AUTHOR  : codeunsolved@gmail.com
# CREATED : August 12 2016
# VERSION : v0.0.1
# UPDATE  : [v0.0.1] September 23 2016
# 1. optimize read_fg_list(); 2. redesign fusion-gene.log("Gene A", "Gene A Seq", "Fusion Part", "Flag|CIGAR", "Gene B", "Gene B Seq", "Fusion Part", "Flag|CIGAR", "Details");
# 3. [important]

from __future__ import division
import os
import re
import sys
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Project.Lib.BASE import get_file_path
from Project.Lib.BASE import read_bed
from Project.Lib.BASE import parse_cigar_len

# CONFIG AREA #
len_primer = 35


def read_fg_list(path_fg_l):
	fg_d = {"fg_a": {}, "fg_b": {}, "ln_b": {}}
	with open(path_fg_l, 'rb') as r_obj_fg:
		for line_fg in r_obj_fg:
			fg_a = re.match('([^\t]+)\t', line_fg).group(1)
			fg_b = re.match('[^\t]+\t([^\t]+)', line_fg).group(1)
			chr_n = re.match('(?:[^\t]+\t){2}([^\t]+)', line_fg).group(1)
			pos_s = int(re.match('(?:[^\t]+\t){3}([^\t]+)', line_fg).group(1))
			pos_e = int(re.match('(?:[^\t]+\t){4}([^\t\n\r]+)', line_fg).group(1))
			if fg_a not in fg_d["ln_b"]:
				fg_d["ln_b"][fg_a] = []
			fg_d["ln_b"][fg_a].append("%s-%s-%s-%s" % (fg_b, chr_n, pos_s, pos_e))
			fg_d["fg_b"]["%s-%s-%s-%s" % (fg_b, chr_n, pos_s, pos_e)] = {"chr": chr_n, "pos_s": pos_s, "pos_e": pos_e}
	for f_key in frag_details:
		chr_n = frag_details[f_key][0]
		gene_name = frag_details[f_key][1]
		pos_s = frag_details[f_key][2]
		pos_e = frag_details[f_key][3]
		if gene_name in fg_d["ln_b"]:
			gene_a_key = "%s-%s-%s-%s" % (gene_name, chr_n, pos_s, pos_e)
			if gene_a_key not in fg_d["fg_a"]:
				fg_d["fg_a"][gene_a_key] = {}
			fg_d["fg_a"][gene_a_key]["chr"] = chr_n
			fg_d["fg_a"][gene_a_key]["pos_s"] = pos_s
			fg_d["fg_a"][gene_a_key]["pos_e"] = pos_e
	return fg_d


def parse_cigar_match_pos(operations, start_pos):
	if re.match('^\d+M$', operations):
		if start_pos != 0:
			return -1
		else:
			return -2
	elif re.match('\d+M', operations):
		return start_pos + 0
	else:
		len_frag = re.match('(\d+)\w', operations).group(1)
		rest_op = operations[len(len_frag) + 1:]
		num_frag = int(len_frag)
		if rest_op:
			return parse_cigar_match_pos(rest_op, start_pos + num_frag)
	return start_pos + num_frag


def get_fusion_direction(val):
	if val == 0:
		return "LEFT"
	elif val == -1:
		return "RIGHT"
	elif val == -2:
		return "FULL"
	elif val > 0:
		return "MIDDLE"


def is_reversed(flag):
	if flag & 0x10:
		return "REVERSE"
	else:
		return ""


def get_fusion_seq(operations, seq):
	if re.match('\d+[MI]', operations):
		len_frag = re.match('(\d+)\w', operations).group(1)
		match_seq = seq[:int(len_frag)]
		return match_seq
	elif re.match('\d+[HD]', operations):
		len_frag = re.match('(\d+)\w', operations).group(1)
		rest_op = operations[len(len_frag) + 1:]
		return get_fusion_seq(rest_op, seq)
	else:
		len_frag = re.match('(\d+)\w', operations).group(1)
		rest_op = operations[len(len_frag) + 1:]
		rest_seq = seq[int(len_frag):]
		return get_fusion_seq(rest_op, rest_seq)


def output_fg(data, dedup_stat, output_name):
	data_sorted = sorted(data, key=lambda d: (d[0], d[1]))
	with open(os.path.join(dir_sam, output_name), 'wb') as w_obj:
		for each_row in data_sorted:
			w_obj.write("%s" % "\t".join([str(x) for x in each_row]))
		w_obj.write("===\tdeDup stat:\t===\n")
		for each_key in dedup_stat:
			w_obj.write("%s\t%d\n" % (each_key, dedup_stat[each_key][0]))
			print "deDup stat: %s - %d" % (each_key, dedup_stat[each_key][0])


if __name__ == '__main__':
	dir_sam = sys.argv[1]
	path_bed = sys.argv[2]
	path_fg_list = sys.argv[3]
	print "========================================================"
	print datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
	print "========================================================"
	print "=>path of *.bed: %s\n=>dir of *.sam: %s\n=>path of fusion gene list: %s" % (path_bed, dir_sam, path_fg_list)

	print "=>get frag details...",
	frag_details = read_bed(path_bed)
	print "OK!"
	# print frag_details

	print "=>get fusion gene list...",
	fg_pair = read_fg_list(path_fg_list)
	print "OK!"
	# print fg_pair

	print "=>get all paths of *.sam file..."
	path_sam_list = get_file_path(dir_sam, "sam", 'list', 2)
	dir_basename = os.path.basename(dir_sam)
	print "OK! total %d." % len(path_sam_list)
	print "========================================================"

	for each_p_sam in path_sam_list:
		print "[No.%d/%d]processing with %s..." % (path_sam_list.index(each_p_sam) + 1, len(path_sam_list), each_p_sam)
		n = 35 if re.match('BRCA', dir_basename) else 0
		with open(each_p_sam, 'rb') as r_obj_sam:
			fg_a_hit = {}
			fg_b_hit = {}
			fg_seq = {}
			fg_output = ["Gene A", "Gene A Seq", "Fusion Part", "Flag|CIGAR", "Gene B", "Gene B Seq", "Fusion Part", "Flag|CIGAR", "Details"]
			fg_dedup = {}
			for line_i, line_sam in enumerate(r_obj_sam):
				if re.match('@', line_sam):
					continue
				qname = re.match('([^\t]+)', line_sam).group(1)
				flag = int(re.match('[^\t]+\t([^\t]+)', line_sam).group(1))
				chr_name = re.match('(?:[^\t]+\t){2}([^\t]+)', line_sam).group(1)
				pos_start = int(re.match('(?:[^\t]+\t){3}([^\t]+)', line_sam).group(1))
				cigar = re.match('(?:[^\t]+\t){5}([^\t]+)', line_sam).group(1)
				seq = re.match('(?:[^\t]+\t){9}([^\t]+)', line_sam).group(1)
				len_match = parse_cigar_len(cigar, 0)
				pos_end = pos_start + len_match - 1

				if qname in fg_seq and len(seq) > fg_seq[qname][0]:
					fg_seq[0] = seq

				for fusion_gene_b in fg_pair["fg_b"]:
					if chr_name == fg_pair["fg_b"][fusion_gene_b]["chr"]:
						if fg_pair["fg_b"][fusion_gene_b]["pos_s"] <= pos_start <= \
								fg_pair["fg_b"][fusion_gene_b]["pos_e"] or \
								fg_pair["fg_b"][fusion_gene_b]["pos_s"] <= pos_end <= \
								fg_pair["fg_b"][fusion_gene_b]["pos_e"]:
							if fusion_gene_b not in fg_b_hit:
								fg_b_hit[fusion_gene_b] = {}
							fg_b_hit[fusion_gene_b][qname] = [flag, cigar, seq]
							if qname not in fg_seq:
								fg_seq[qname] = [seq]
							fg_seq[qname].append(line_sam)
							break
				for fusion_gene_a in fg_pair["fg_a"]:
					if chr_name == fg_pair["fg_a"][fusion_gene_a]["chr"]:
						if fg_pair["fg_a"][fusion_gene_a]["pos_s"] <= pos_start <= \
								fg_pair["fg_a"][fusion_gene_a]["pos_e"] or \
								fg_pair["fg_a"][fusion_gene_a]["pos_s"] <= pos_end <= \
								fg_pair["fg_a"][fusion_gene_a]["pos_e"]:
							if fusion_gene_a not in fg_a_hit:
								fg_a_hit[fusion_gene_a] = {}
							fg_a_hit[fusion_gene_a][qname] = [flag, cigar, seq]
							if qname not in fg_seq:
								fg_seq[qname] = [seq]
							fg_seq[qname].append(line_sam)
							break

			for fg_a in fg_a_hit:
				for fg_a_sn in fg_a_hit[fg_a]:
					gene_a_name = re.match('([^-]+)\-', fg_a).group(1)
					for fg_b in fg_pair["ln_b"][gene_a_name]:
						if fg_b in fg_b_hit:
							for fg_b_sn in fg_b_hit[fg_b]:
								if fg_a_sn == fg_b_sn:
									fg_a_flag = fg_a_hit[fg_a][fg_a_sn][0]
									fg_a_cigar = fg_a_hit[fg_a][fg_a_sn][1]
									fg_a_seq = fg_a_hit[fg_a][fg_a_sn][2]
									fg_b_flag = fg_b_hit[fg_b][fg_b_sn][0]
									fg_b_cigar = fg_b_hit[fg_b][fg_b_sn][1]
									fg_b_seq = fg_b_hit[fg_b][fg_b_sn][2]
									#print "A: %s-%s-%s" % (fg_a_flag, fg_a_cigar, fg_a_seq)
									#print "B: %s-%s-%s" % (fg_b_flag, fg_b_cigar, fg_b_seq)

									fusion_direct_a = get_fusion_direction(parse_cigar_match_pos(fg_a_cigar, 0))
									fusion_direct_b = get_fusion_direction(parse_cigar_match_pos(fg_b_cigar, 0))
									fusion_part_a = fusion_direct_a + " | " + is_reversed(fg_a_flag) if is_reversed(fg_a_flag) else fusion_direct_a
									fusion_part_b = fusion_direct_b + " | " + is_reversed(fg_b_flag) if is_reversed(fg_b_flag) else fusion_direct_b

									fusion_seq_a = get_fusion_seq(fg_a_cigar, fg_a_seq)
									fusion_seq_b = get_fusion_seq(fg_b_cigar, fg_b_seq)

									fg_output.append([fg_a, fusion_part_a, str(fg_a_flag) + " | " + fg_a_cigar,
													  fg_b, fusion_part_b, str(fg_b_flag) + " | " + fg_b_cigar,
													  "\t".join([re.sub('[\t\n]', ' ', str(x)) for x in fg_seq[fg_a_sn]])])

									key_name = "%s-%s-%s-%s" % (gene_a_name, re.match('([^-]+)\-', fg_b).group(1),
										fg_pair["fg_b"][fg_b]["chr"], fg_pair["fg_b"][fg_b]["pos_s"])
									if key_name not in fg_dedup:
										fg_dedup[key_name] = [1, fg_seq[fg_a_sn]]
									if fg_seq[fg_a_sn] not in fg_dedup[key_name]:
										fg_dedup[key_name].append(fg_seq[fg_a_sn])
										fg_dedup[key_name][0] += 1
									print "got fusion gene: %s" % ("  ".join([fg_a, fusion_part_a, str(fg_a_flag) + " | " + fg_a_cigar,
																			  fg_b, fusion_part_b, str(fg_b_flag) + " | " + fg_b_cigar]))

		print "output fusion-gene log..."
		output_filename = "%s-fusion-gene.log" % re.match('(.+)\.sam', os.path.basename(each_p_sam)).group(1)
		if fg_output:
			output_fg(fg_output, fg_dedup, output_filename)
		else:
			print "No fusion gene marked!"
		print "========================================================\nOK!"
