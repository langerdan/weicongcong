#!/bin/zsh

r1=$1
r2=$2
if [[ $# -eq 3 ]]; then
	log_name=$3
else
	log_name="Mapping"
fi

MAPPINGTIME=`python -c 'import time; print time.time()'`
ref_genome=/Users/codeunsolved/NGS/RefGenome/UCSC/hg19/hg19
echo "\033[1;36m=>RefGenome: $ref_genome\033[0m"

r1_filename=$(basename $r1)
r2_filename=$(basename $r2)
echo "\033[1;36m=>r1's filename: $r1_filename\n=>r2's filename: $r2_filename\033[0m"

r_dir=$(dirname $r1)
log=${r_dir}/${log_name}.log

if [[ $r1_filename =~ '^(.+)_R[12]' ]]; then
	r_basename=$match[1]
	echo "\033[1;36m=>reads' basename: $r_basename\033[0m"
else
	echo "\033[1;33m[WARNING]can not detect 'R1'/'R2' identifer in reads' filename, use 'sample' instead!\033[0m"
	r_basename='sample'
fi

r_path=${r_dir}/$r_basename
echo "\033[1;36m=>output path: $r_path"

printf "\033[1;36m[STEP 1/3]output SAM...\033[0m\n"
bwa mem -t 3 -M $ref_genome $r1 $r2 >${r_path}.sam
printf "\033[1;32mOK!\033[0m\n"

printf "\033[1;36m[STEP 2/3]trans SAM to BAM and sort BAM...\033[0m"
samtools view -bhS ${r_path}.sam | samtools sort - >${r_path}.sort.bam
printf "\033[1;32mOK!\033[0m\n"

printf "\033[1;36m[STEP 3/3]index BAM...\033[0m"
samtools index ${r_path}.sort.bam >${r_path}.sort.bam.bai
printf "\033[1;32mOK!\033[0m\n"

echo "========================================================"
echo "Mapping time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$MAPPINGTIME")s | tee -a $log
echo "========================================================"