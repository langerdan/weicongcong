#!/bin/zsh

dir=$1
bed=$2

for file in `ls $dir`
do
    echo $file
    if [[ $file =~ '(.+)_R[1](.+\.fastq.gz)$' ]]; then
        basename=$match[1]
        restname=$match[2]

        r1=${dir}/$file
        r2=${dir}/${basename}_R2$restname
        echo "=>r1's path:$r1\n=>r2's path:$r2"

        r_dirname=$(dirname $r1)
        log=${r_dirname}/preVarantCalling.log

        STARTTIME=$(date +%s000)

        # `wc -c < $file` outputs number with a preceding space
        # but it has no problem with calculate
        # use `wc -c $file | awk '{print $1}'` can fix that
        r1_size=`wc -c < $r1`
        r2_size=`wc -c < $r2`
        echo "========================================================"
        echo "$r1_filename size: "`bc -l <<< "scale=2; $r1_filename/1024/1024"`MB | tee -a log
        echo "$r2_filename size: "`bc -l <<< "scale=2; $r2_filename/1024/1024"`MB | tee -a log
        echo "========================================================"

        echo "<< FASTQC >>"
        fastqc $r1 $r2 -o $r_dirname
        echo "========================================================"
        echo "initQC time: "`bc -l <<< "scale=2; $(date +%s000)-$STARTTIMEt"`s | tee -a log
        echo "========================================================"

        echo "<< BWA >>"
        ./mapping.sh $r1 $r2
    fi
done

cd $r_dirname

echo "<< samtools depth >>"
com-with "samtools depth -a -b $2" "ls *.bam" ">#bam#depth"
echo "========================================================"
echo "samtools depth time: "`bc -l <<< "scale=2; $(date +%s000)-$STARTTIMEt"`s| tee -a log
echo "========================================================"

echo "<< samtools stats >>"
com-with "samtools stats -c" "ls *.bam" ">#bam#stats"
echo "========================================================"
echo "samtools stats time: "`bc -l <<< "scale=2; $(date +%s000)-$STARTTIMEt"`s| tee -a log
echo "========================================================"

echo "========================================================"
echo "Total time: "`bc -l <<< "scale=2; $(date +%s000)-$STARTTIMEt"`s| tee -a log
echo "Total time: "`bc -l <<< "scale=2; ($(date +%s000)-$STARTTIMEt)/3600"`h| tee -a log
echo "========================================================"