#!/bin/zsh

dir_output=$1
dir_basename=$(basename $dir_output)

dir_report=~/Downloads/NGS-Data/Report-reads_counts/
echo "=>processing report copy from \"$dir_output\" to \"$dir_report\"..."
if [[ -d ${dir_report}/${dir_basename} ]]; then
    echo "[WARNING] ${dir_report}/${dir_basename} existed! delete ..."
    rm -rf ${dir_report}/${dir_basename}
fi
echo "=>Command: mkdir ${dir_report}/${dir_basename}"
mkdir ${dir_report}/${dir_basename}
echo "=>Command: cp ${dir_output}/reads_stat* ${dir_report}/${dir_basename}"
cp ${dir_output}/reads_stat* ${dir_report}/${dir_basename}
