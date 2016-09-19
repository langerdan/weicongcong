#!/bin/zsh

r1=$1
r2=$2
echo "paired end reads: $r1, $r2"
qn=$3
echo "qc filter: $3"
echo 'output qc by fastqc...'
fastqc $r1 $r2
echo 'done!'
echo 'filter qc by IlluQC.pl..'
perl /Users/codeunsolved/NGS/soft/NGSQCToolkit_v2.3.3/QC/IlluQC.pl -pe $r1 $r2 N A -s $qn
echo 'done!'
