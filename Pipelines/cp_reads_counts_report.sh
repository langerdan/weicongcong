#!/bin/zsh

dir_output=$1
dir_basename=$(basename $dir_output)

dir_report=~/Downloads/NGS-Data/Report-reads_counts/
echo "\033[1;36m=>copy report from \"$dir_output\" to \"$dir_report\"...\033[0m"
if [[ -d ${dir_report}/${dir_basename} ]]; then
	echo "\033[1;33m[WARNING] ${dir_report}/${dir_basename} existed! delete ...\033[0m"
	rm -rf ${dir_report}/${dir_basename}
fi
echo "\033[1;36m=>Command: mkdir ${dir_report}/${dir_basename}\033[0m"
mkdir ${dir_report}/${dir_basename}
echo "\033[1;36m=>Command: cp ${dir_output}/reads_stat* ${dir_report}/${dir_basename}\033[0m"
cp ${dir_output}/reads_stat* ${dir_report}/${dir_basename}
