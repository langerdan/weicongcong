#!/bin/zsh

r1=$1
r2=$2
genome=/Users/codeunsolved/NGS/RefGenome/UCSC/hg19/hg19
echo "=>r1:$r1 r2:$r2"
echo "=>genome: $genome"

rx_basename=0
p_dir=0
function getBasename(){
    if [[ $1 =~ '^(.*/)(.+)\.[^\.]+$' ]];
    then
        p_dir=$match[1]
        rx_basename=$match[2]
    elif [[ $1 =~ '^(.+)\.[^\.]+$' ]];
    then
        p_dir=./
        rx_basename=$match[1]
    fi
    echo "=>$2's basename seems like: $rx_basename"
}

getBasename $r1 r1
r1_basename=$rx_basename
getBasename $r2 r2
r2_baseanme=$rx_basename

if [[ $r1_basename =~ '^(.+)_R[12]' ]];
then
    r_basename=$match[1]
    echo "=>reads' basename seems like: $r_basename"
else
    echo "[WARNING]can not detect 'R1'/'R2' identifer in reads' name, use 'sample' instead!"
    r_basename='sample'
fi

r_path=${p_dir}$r_basename
echo "=>output path: $r_path"

printf "[STEP 1/4]output SAM..."
bwa mem -t 4 -M $genome $r1 $r2 >${r_path}.sam
printf "OK!\n"

printf "[STEP 2/4]trans SAM to BAM..."
samtools view -bhS ${r_path}.sam >${r_path}.bam
printf "OK!\n"

printf "[STEP 3/4]sort BAM..."
samtools sort ${r_path}.bam >${r_path}.sort.bam
printf "OK!\n"

printf "[STEP 4/4]index BAM..."
samtools index ${r_path}.sort.bam >${r_path}.sort.bam.bai
printf "OK!\n"

echo "=============================================="
echo "Done!"

