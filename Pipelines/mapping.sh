#!/bin/zsh

r1=$1
r2=$2

MAPPINGTIME=`python -c 'import time; print time.time()'`
ref_genome=/Users/codeunsolved/NGS/RefGenome/UCSC/hg19/hg19
echo "=>RefGenome: $ref_genome"

r1_filename=$(basename $r1)
r2_filename=$(basename $r2)
echo "=>r1's filename: $r1_filename\n=>r2's filename: $r2_filename"

r_dir=$(dirname $r1)
log=${r_dir}/preVarantCalling.log

if [[ $r1_filename =~ '^(.+)_R[12]' ]]; then
    r_basename=$match[1]
    echo "=>reads' basename: $r_basename"
else
    echo "[WARNING]can not detect 'R1'/'R2' identifer in reads' filename, use 'sample' instead!"
    r_basename='sample'
fi

r_path=${r_dir}/$r_basename
echo "=>output path: $r_path"

printf "[STEP 1/3]output SAM..."
bwa mem -t 3 -M $ref_genome $r1 $r2 >${r_path}.sam
printf "OK!\n"

printf "[STEP 2/3]trans SAM to BAM and sort BAM..."
samtools view -bhS ${r_path}.sam | samtools sort - >${r_path}.sort.bam
printf "OK!\n"

printf "[STEP 3/3]index BAM..."
samtools index ${r_path}.sort.bam >${r_path}.sort.bam.bai
printf "OK!\n"

echo "========================================================"
echo "Mapping time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$MAPPINGTIME")s | tee -a $log
echo "========================================================"