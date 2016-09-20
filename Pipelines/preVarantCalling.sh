#!/bin/zsh

dir_data=$1
bed=$2

STARTTIME=`python -c 'import time; print time.time()'`

log=${dir_data}/preVarantCalling.log
echo -n "" >$log
echo "========================================================"
echo $(date) | tee -a $log
echo "========================================================"

for file in `ls $dir_data`
do
    if [[ $file =~ '(.+)_R1(.+\.fastq(\.gz)?)$' ]]; then
        basename=$match[1]
        restname=$match[2]

        r1=${dir_data}/$file
        r2=${dir_data}/${basename}_R2$restname
        echo "=>r1's path:$r1\n=>r2's path:$r2"
        r1_filename=$(basename $r1)
        r2_filename=$(basename $r2)

        # `wc -c < $file` outputs number with a preceding space
        # but it has no problem with calculate
        # use `wc -c $file | awk '{print $1}'` can fix that
        r1_size=`wc -c < $r1`
        r2_size=`wc -c < $r2`
        echo "========================================================"
        echo "$r1_filename size: "`bc -l <<< "scale=2; $r1_size/1024/1024"`MB | tee -a $log
        echo "$r2_filename size: "`bc -l <<< "scale=2; $r2_size/1024/1024"`MB | tee -a $log
        echo "========================================================"

        echo "<< FASTQC >>"
        FASTQCTIME=`python -c 'import time; print time.time()'`
        fastqc $r1 $r2 -o $dir_data
        echo "========================================================"
        echo "FASTQC time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$FASTQCTIME")s | tee -a $log
        echo "========================================================"

        echo "<< BWA >>"
        ./mapping.sh $r1 $r2
    else
        echo "PASS $file"
    fi
done

cd $dir_data

echo "<< samtools depth >>"
SAMDTIME=`python -c 'import time; print time.time()'`
com-with "samtools depth -a -b $2" "ls *.bam" ">#bam#depth"
echo "========================================================"
echo "samtools depth time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$SAMDTIME")s| tee -a $log
echo "========================================================"

echo "<< samtools stats >>"
SAMSTIME=`python -c 'import time; print time.time()'`
com-with "samtools stats -c" "ls *.bam" ">#bam#stats"
echo "========================================================"
echo "samtools stats time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$SAMSTIME")s| tee -a $log
echo "========================================================"

echo "========================================================"
echo "Total time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$STARTTIME")s| tee -a $log
echo "Total time: "$(bc -l <<< "scale=2; (`python -c 'import time; print time.time()'`-$STARTTIME)/3600")h| tee -a $log
echo "========================================================"