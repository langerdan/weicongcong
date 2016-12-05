#!/bin/zsh
# -*- coding: utf-8 -*-
# PROGRAM : preVarantCalling
# AUTHOR  : codeunsolved@gmail.com
# CREATED : Spetember 21 2016
# VERSION : v0.0.1a

option=$1
dir_data=$2
bed=$3
f_g_list=$4

STARTTIME=`python -c 'import time; print time.time()'`

dir_ngs_manaul=`echo ~/NGS/NGS-Manual`
log=${dir_data}/preVarantCalling.log

if [[ $option =~ 'new' ]]; then
	echo -n "" >$log
fi
echo "========================================================" | tee -a $log
echo $(date) | tee -a $log
echo "========================================================" | tee -a $log

for file in `ls $dir_data`
do
	if [[ $file =~ '^(.+)_R1(.+\.fastq(\.gz)?)$' ]]; then
		basename=$match[1]
		restname=$match[2]

		r1=${dir_data}/$file
		r2=${dir_data}/${basename}_R2$restname
		echo "\033[1;36m=>R1's path:$r1\n=>R2's path:$r2\033[0m"
		r1_filename=$(basename $r1)
		r2_filename=$(basename $r2)

		# `wc -c < $file` outputs number with a preceding space
		# but it has no problem with calculate
		# use `wc -c $file | awk '{print $1}'` can fix that
		r1_size=`wc -c < $r1`
		r2_size=`wc -c < $r2`
		echo "========================================================"
		echo "$r1_filename SIZE: "`bc -l <<< "scale=2; $r1_size/1024/1024"`MB | tee -a $log
		echo "$r2_filename SIZE: "`bc -l <<< "scale=2; $r2_size/1024/1024"`MB | tee -a $log
		echo "========================================================"

		if [[ $option =~ 'fastqc' ]]; then
			echo "\033[1;36m<< FASTQC >>\033[0m"
			FASTQCTIME=`python -c 'import time; print time.time()'`
			fastqc $r1 $r2 -o $dir_data -q
			echo "========================================================"
			echo "FASTQC time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$FASTQCTIME")s | tee -a $log
			echo "========================================================"
		fi
		
		if [[ $option =~ 'bwa' ]]; then
			echo "\033[1;36m<< BWA >>\033[0m"
			${dir_ngs_manaul}/Pipelines/mapping.sh $r1 $r2 "preVarantCalling"
		fi
	else
		echo "\033[1;30m*PASS* $file\033[0m"
	fi
done

if [[ $option =~ 'stat' ]]; then
	echo "\033[1;36m<< samtools stats >>\033[0m"
	SAMSTIME=`python -c 'import time; print time.time()'`
	if [[ -n `echo $dir_data/*.sort.bam` ]]; then
		com-with "samtools stats" "ls ${dir_data}/*.sort.bam" %@${dir_data}@#sort.bam#stats
		com-with "samtools view -b -L $bed" "ls ${dir_data}/*.sort.bam" %@${dir_data}@#sort.bam#target.stats "samtools stats"
	else
		com-with "samtools stats" "ls ${dir_data}/*.bam" %@${dir_data}@#bam#stats
		com-with "samtools view -b -L $bed" "ls ${dir_data}/*.bam" %@${dir_data}@#bam#target.stats "samtools stats"
	fi
	echo "========================================================"
	echo "samtools stats time: $(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$SAMSTIME")s" | tee -a $log
	echo "========================================================"
fi

if [[ $option =~ 'depth' ]]; then
	echo "\033[1;36m<< samtools depth >>\033[0m"
	SAMDTIME=`python -c 'import time; print time.time()'`
	if [[ -n `echo $dir_data/*.sort.bam` ]]; then
		com-with "samtools depth -a -b $bed" "ls ${dir_data}/*.sort.bam" %@${dir_data}@#sort.bam#depth
	else
		com-with "samtools depth -a -b $bed" "ls ${dir_data}/*.bam" %@${dir_data}@#bam#depth
	fi
	echo "========================================================"
	echo "samtools depth time: $(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$SAMDTIME")s" | tee -a $log
	echo "========================================================"
fi

if [[ $option =~ 'toSAM' ]]; then
	echo "\033[1;36m<< BAM to SAM >>\033[0m"
	TOSAMTIME=`python -c 'import time; print time.time()'`
	if [[ -n `echo $dir_data/*.sort.bam` ]]; then
		com-with "samtools view -h" "ls ${dir_data}/*.sort.bam" %@${dir_data}@#sort.bam#sam
	else
		com-with "samtools view -h" "ls ${dir_data}/*.bam" %@${dir_data}@#bam#sam
	fi
	echo "========================================================"
	echo "BAM to SAM time: $(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$TOSAMTIME")s" | tee -a $log
	echo "========================================================"
fi

if [[ $option =~ 'reads' ]]; then
	echo "\033[1;36m<< reads count stat >>\033[0m"
	RDCSTIME=`python -c 'import time; print time.time()'`
	python ${dir_ngs_manaul}/Project/countReads.py $dir_data $bed
	${dir_ngs_manaul}/Pipelines/cp_reads_counts_report.sh $dir_data
	echo "========================================================"
	echo "reads count stat time: $(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$RDCSTIME")s" | tee -a $log
	echo "========================================================"
fi

if [[ $option =~ 'fusiongene' ]]; then
	echo "\033[1;36m<< mark fusion gene >>\033[0m"
	MFGTIME=`python -c 'import time; print time.time()'`
	python ${dir_ngs_manaul}/Project/FusionGene/markFusionGene.py $dir_data $bed $f_g_list
	${dir_ngs_manaul}/Pipelines/cp_fusion_gene_log.sh $dir_data
	echo "========================================================"
	echo "mark fusion gene time: $(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$MFGTIME")s" | tee -a $log
	echo "========================================================"
fi

echo "Total time: $(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$STARTTIME")s" | tee -a $log
echo "Total time: $(bc -l <<< "scale=2; (`python -c 'import time; print time.time()'`-$STARTTIME)/3600")h" | tee -a $log
echo "========================================================"
${dir_ngs_manaul}/Pipelines/doneReminder.sh "preVarantCalling complete!"