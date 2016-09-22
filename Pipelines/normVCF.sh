#!/bin/zsh

dir_vcf=$1
dir_output=$1/normVCF
if [[ !(-d $dir_output) ]]; then
	mkdir $dir_output
fi
ref_genome=/Users/codeunsolved/NGS/RefGenome/UCSC/hg19/hg19.fa
echo "=>dir_vcf: $dir_vcf\n=>dir_output: $dir_output\n=>RefGenome: $ref_genome"

for file in `ls $dir_vcf`
do
	if [[ $file =~ '^(.+)\.vcf$' ]]; then
		vcf_basename=$match[1]
		echo "=>vcf' basename seems like: $vcf_basename"
		bcftools norm -m-both -o $dir_output/$vcf_basename.split.vcf $dir_vcf/$file
		bcftools norm -f $ref_genome -o $dir_output/$vcf_basename.norm.vcf $dir_output/$vcf_basename.split.vcf
	else
		echo "[WARNING]can not detect '.vcf' suffix in '$file', PASS!"
	fi
done