#!/bin/zsh

dir_output=$1
dir_basename=$(basename $dir_output)

dir_report=~/Downloads/NGS-Data/Report-fusion_gene/
echo "\033[1;36m=>copy FusionGene log from \"$dir_output\" to \"$dir_report\"...\033[0m"
if [[ -d ${dir_report}/${dir_basename} ]]; then
	echo "\033[1;33m[WARNING] ${dir_report}/${dir_basename} existed! ignore ...\033[0m"
else
	echo "\033[1;33m[WARNING] ${dir_report}/${dir_basename} is not existed! create ...\033[0m"
	echo "\033[1;36m=>Command: mkdir ${dir_report}/${dir_basename}\033[0m"
	mkdir ${dir_report}/${dir_basename}
fi

echo "\033[1;36m=>Command: cp ${dir_output}/*fusion-gene.log ${dir_report}/${dir_basename}\033[0m"
cp ${dir_output}/*fusion-gene.log ${dir_report}/${dir_basename}
