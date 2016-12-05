#!/bin/zsh
# -*- coding: utf-8 -*-
# PROGRAM : handleOutbox
# AUTHOR  : codeunsolved@gmail.com
# CREATED : November 30 2016
# VERSION : v0.0.1a

project_prefix=$1
run_bn=$2
dir_data=$3
dir_output=$4
bed=$5
option=$6

if [[ ! -x $dir_output ]]; then
	echo "\033[1;33m$dir_output doesn't exsist, create it!\033[0m"
	mkdir $dir_output
fi

STARTTIME=`python -c 'import time; print time.time()'`

echo "========================================================"
echo $(date)
echo "========================================================"

echo "\033[1;32m=>Project:\033[0m $project_prefix"
echo "\033[1;32m=>RUN:\033[0m $run_bn\n\033[1;32m=>dir_data:\033[0m $dir_data"
echo "\033[1;32m=>dir_output:\033[0m $dir_output\n\033[1;32m=>bed:\033[0m $bed"
echo "========================================================"

if [[ $option =~ 'pull' ]]; then
	echo "\033[1;36m<< pullOutbox >>\033[0m"
	PULLOUTBOX=`python -c 'import time; print time.time()'`
	pullOutbox $dir_data $dir_output
	echo "========================================================"
	echo "pullOutbox time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$PULLOUTBOX")s
	echo "========================================================"

	echo "\033[1;36m<< pullMiSeq >>\033[0m"
	PULLMISEQ=`python -c 'import time; print time.time()'`
	python ~/NGS/Topgen-Dashboard/py/pullMiSeq.py $run_bn $dir_output
	echo "========================================================"
	echo "pullMiSeq time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$PULLMISEQ")s
	echo "========================================================"
fi

if [[ $option =~ 'cross' ]]; then
	CROSSSNP=`python -c 'import time; print time.time()'`
	echo "\033[1;36m<< crossSNP >>\033[0m"
	python ~/NGS/Topgen-Dashboard/py/crossSNP.py autobox $project_prefix $run_bn -ic
	echo "========================================================"
	echo "Cross SNP time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$CROSSSNP")s
	echo "========================================================"
fi

if [[ $option =~ 'miss' ]]; then
	CHECKMISSING=`python -c 'import time; print time.time()'`
	echo "\033[1;36m<< checkMissing >>\033[0m"
	python ~/NGS/Topgen-Dashboard/py/checkMissing.py autobox $dir_data $project_prefix $run_bn
	echo "========================================================"
	echo "Check Missing time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$CHECKMISSING")s
	echo "========================================================"
fi

if [[ $option =~ 'prevc' ]]; then
	echo "\033[1;36m<< preVarantCalling >>\033[0m"
	preVarantCalling ${option}fastqcdepthstat $dir_output $bed /Users/codeunsolved/Downloads/NGS-Data/bed/fusion_gene_listv1.2
fi

if [[ $option =~ 'qc' ]]; then
	QCREPORTER=`python -c 'import time; print time.time()'`
	echo "\033[1;36m<< QC Reporter >>\033[0m"
	python ~/NGS/Topgen-Dashboard/py/QC_Reporter.py $dir_output $bed
	echo "========================================================"
	echo "QC Reporter time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$QCREPORTER")s
	echo "========================================================"
fi
