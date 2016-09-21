#!/bin/zsh

option=$1
dir_data=$2
bed=$3
f_g_list=$4

STARTTIME=`python -c 'import time; print time.time()'`

log=${dir_data}/SeqDataQC.log
echo -n "" >$log
echo "========================================================"
echo $(date) | tee -a $log
echo "========================================================"

for file in `ls $dir_data`
do
    if [[ $file =~ '^(.+)_R1(.+\.fastq(\.gz)?)$' ]]; then
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

        if [[ $option =~ 'fastqc' ]]; then
            echo "<< FASTQC >>"
            FASTQCTIME=`python -c 'import time; print time.time()'`
            fastqc $r1 $r2 -o $dir_data
            echo "========================================================"
            echo "FASTQC time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$FASTQCTIME")s | tee -a $log
            echo "========================================================"
        fi
        
        if [[ $option =~ 'bwa' ]]; then
            echo "<< BWA >>"
            ./mapping.sh $r1 $r2 "preVarantCalling"
        fi
    else
        echo "*PASS* $file"
    fi
done

cd $dir_data

echo "<< samtools stats >>"
SAMSTIME=`python -c 'import time; print time.time()'`
if [[ -n `echo $dir_data/*.sort.bam` ]]; then
    com-with "samtools stats" "ls *.sort.bam" ">#sort.bam#stats"
else
    com-with "samtools stats" "ls *.bam" ">#bam#stats"
fi
echo "========================================================"
echo "samtools stats time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$SAMSTIME")s| tee -a $log
echo "========================================================"

if [[ $option =~ 'depth' ]]; then
    echo "<< samtools depth >>"
    SAMDTIME=`python -c 'import time; print time.time()'`
    if [[ -n `echo $dir_data/*.sort.bam` ]]; then
        com-with "samtools depth -a -b $2" "ls *.sort.bam" ">#sort.bam#depth"
    else
        com-with "samtools depth -a -b $2" "ls *.bam" ">#bam#depth"
    fi
    echo "========================================================"
    echo "samtools depth time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$SAMDTIME")s| tee -a $log
    echo "========================================================"
fi

if [[ $option =~ 'brca' ]]; then
    echo "<< reads count stat >>"
    RDCSTIME=`python -c 'import time; print time.time()'`
    python /Users/codeunsolved/NGS/NGS-Manual/Project/countReads.py $dir_data $bed
    echo "========================================================"
    echo "reads count stat time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$RDCSTIME")s| tee -a $log
    echo "========================================================"
    cp-reads-counts-report $dir_data
elif [[ $option =~ 'onco' ]]; then
    echo "<< mark fusion gene >>"
    MFGTIME=`python -c 'import time; print time.time()'`
    python /Users/codeunsolved/NGS/NGS-Manual/Project/FusionGene/markFusionGene.py $dir_data $bed $f_g_list
    echo "========================================================"
    echo "mark fusion gene time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$MFGTIME")s| tee -a $log
    echo "========================================================"
fi

echo "========================================================"
echo "Total time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$STARTTIME")s| tee -a $log
echo "Total time: "$(bc -l <<< "scale=2; (`python -c 'import time; print time.time()'`-$STARTTIME)/3600")h| tee -a $log
echo "========================================================"
doneRemind "preVarantCalling done!"