#!/bin/zsh

r1=$1
r2=$2
echo "\033[1;36m=>paired end reads: $r1, $r2\033[0m"
qn=$3
echo "\033[1;36m=>qc filter: $3\033[0m"
echo "\033[1;36m=>output qc by fastqc...\033[0m"
fastqc $r1 $r2
echo "done!"
echo "\033[1;36m=>filter Q$qn by IlluQC.pl..\033[0m"
perl /Users/codeunsolved/NGS/soft/NGSQCToolkit_v2.3.3/QC/IlluQC.pl -pe $r1 $r2 N A -s $qn
echo "done!"
