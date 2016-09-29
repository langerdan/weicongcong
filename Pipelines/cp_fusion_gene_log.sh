#!/bin/zsh
# -*- coding: utf-8 -*-
# PROGRAM : cp_fusion_gene_log
# AUTHOR  : codeunsolved@gmail.com
# CREATED : September 6 2016
# VERSION : v0.0.1a

dir_output=$1
dir_basename=$(basename $dir_output)

dir_report=~/Downloads/NGS-Data/Report-fusion_gene/
echo "\033[1;36m=>copy FusionGene log from \"$dir_output\" to \"$dir_report\"...\033[0m"
if [[ -d ${dir_report}/${dir_basename} ]]; then
	echo "\033[1;33m[WARNING] dir existed! ignore: ${dir_report}/${dir_basename}\033[0m"
else
	echo "\033[1;33m[WARNING] dir is not existed! create: ${dir_report}/${dir_basename}\033[0m"
	echo "\033[1;36m=>Command: mkdir ${dir_report}/${dir_basename}\033[0m"
	mkdir ${dir_report}/${dir_basename}
fi

echo "\033[1;36m=>Command: cp ${dir_output}/*fusion-gene.log ${dir_report}/${dir_basename}\033[0m"
cp ${dir_output}/*fusion-gene.log ${dir_report}/${dir_basename}
