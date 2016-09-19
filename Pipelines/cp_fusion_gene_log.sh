#!/bin/zsh

dir_output=$1
dir_basename=$(basename $dir_output)

dir_report=~/Downloads/NGS-Data/Report-fusion_gene/
echo "=>processing FusionGene log copy from \"$dir_output\" to \"$dir_report\"..."
if [[ -d ${dir_report}/${dir_basename} ]]; then
    echo "[WARNING] ${dir_report}/${dir_basename} existed! ignore ..."
else
    echo "[WARNING] ${dir_report}/${dir_basename} is not existed! create ..."
    echo "=>Command: mkdir ${dir_report}/${dir_basename}"
    mkdir ${dir_report}/${dir_basename}
fi

echo "=>Command: cp ${dir_output}/*fusion-gene.log ${dir_report}/${dir_basename}"
cp ${dir_output}/*fusion-gene.log ${dir_report}/${dir_basename}
