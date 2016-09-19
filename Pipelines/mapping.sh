#!/bin/zsh

r1=$1
r2=$2
ref_genome=/Users/codeunsolved/NGS/RefGenome/UCSC/hg19/hg19

STARTTIME=$(date +%s000)
echo "=>RefGenome: $ref_genome"

r1_filename=$(basename $r1)
r2_filename=$(basename $r2)
echo "=>r1's basename: $r1_filename\n=>r2's basename: $r2_filename"

r_dirname=$(dirname $r1)
log=${r_dirname}/preVarantCalling.log

if [[ $r1_filename =~ '^(.+)_R[12]' ]]; then
    r_basename=$match[1]
    echo "=>reads' basename: $r_basename"
else
    echo "[WARNING]can not detect 'R1'/'R2' identifer in reads' filename, use 'sample' instead!"
    r_basename='sample'
fi

r_path=${r_dirname}/$r_basename
echo "=>output path: $r_path"

printf "[STEP 1/4]output SAM..."
bwa mem -t 3 -M $ref_genome $r1 $r2 >${r_path}.sam
printf "OK!\n"

printf "[STEP 2/4]trans SAM to BAM..."
printf "[STEP 3/4]sort BAM..."
samtools view -bhS ${r_path}.sam | samtools sort - >${r_path}.sort.bam
printf "OK!\n"

printf "[STEP 4/4]index BAM..."
samtools index ${r_path}.sort.bam >${r_path}.sort.bam.bai
printf "OK!\n"

echo "========================================================"
echo "Mapping time: "`bc -l <<< "scale=2; $(date +%s000)-$STARTTIMEt"`s | tee -a log
echo "========================================================"
