# Data Preprocessing

> ***Version:*** v0.01a
>
> ***Author:*** codeunsolved@gmail.com
>
> ***Created:*** July 20 2016



## 1.  Init QC

+ Soft version:
  + FastQC *v0.11.5*
  + NGSToolkit *v2.3.3*



### 1.1 FastQC

```shell
fastqc $r1 $r2
```



### 1.2 NGSToolkit

```shell
IlluQC.pl -pe $r1 $r2 N A -s $qn
```

> **-pe** *<Forward reads file> <Reverse reads file> <Primer/Adaptor library> <FASTQ variant>*
>
> > **Primer/Adaptor libraries:**
> >
> >  1 = Genomic DNA/Chip-seq Library
> >  2 = Paired End DNA Library
> >  3 = DpnII gene expression Library
> >  4 = NlaIII gene expression Library
> >  5 = Small RNA Library
> >  6 = Multiplexing DNA Library
> >  N = Do not filter for Primer/Adaptor
> >  <File> = File for user defined primer/adaptor sequences, one per line
> >
> > 
> >
> >  **FASTQ variants:**
> >  1 = Sanger (Phred+33, 33 to 73)
> >  2 = Solexa (Phred+64, 59 to 104)
> >  3 = Illumina (1.3+) (Phred+64, 64 to 104)
> >  4 = Illumina (1.5+) (Phred+64, 66 to 104)
> >  5 = Illumina (1.8+) (Phred+33, 33 to 74)
> >  A = Automatic detection of FASTQ variant
>
> 
>
> **-s** | -cutOffQualScore *<Integer, 0 to 40>*
>  The cut-off value for PHRED quality score for high-quality
> filtering
>  **default: 20**



### 1.3 Bash Pipeline

```shell
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
```



**Output:**

```
script/qc_init.sh 008-F08_S5_L001_R1_001.fastq 008-F08_S5_L001_R2_001.fastq 30
paired end reads: 008-F08_S5_L001_R1_001.fastq, 008-F08_S5_L001_R2_001.fastq
qc filter: 30
output qc by fastqc...
Started analysis of 008-F08_S5_L001_R1_001.fastq
Approx 5% complete for 008-F08_S5_L001_R1_001.fastq
Approx 10% complete for 008-F08_S5_L001_R1_001.fastq
Approx 15% complete for 008-F08_S5_L001_R1_001.fastq
Approx 20% complete for 008-F08_S5_L001_R1_001.fastq
Approx 25% complete for 008-F08_S5_L001_R1_001.fastq
Approx 30% complete for 008-F08_S5_L001_R1_001.fastq
Approx 35% complete for 008-F08_S5_L001_R1_001.fastq
Approx 40% complete for 008-F08_S5_L001_R1_001.fastq
Approx 45% complete for 008-F08_S5_L001_R1_001.fastq
Approx 50% complete for 008-F08_S5_L001_R1_001.fastq
Approx 55% complete for 008-F08_S5_L001_R1_001.fastq
Approx 60% complete for 008-F08_S5_L001_R1_001.fastq
Approx 65% complete for 008-F08_S5_L001_R1_001.fastq
Approx 70% complete for 008-F08_S5_L001_R1_001.fastq
Approx 75% complete for 008-F08_S5_L001_R1_001.fastq
Approx 80% complete for 008-F08_S5_L001_R1_001.fastq
Approx 85% complete for 008-F08_S5_L001_R1_001.fastq
Approx 90% complete for 008-F08_S5_L001_R1_001.fastq
Approx 95% complete for 008-F08_S5_L001_R1_001.fastq
Analysis complete for 008-F08_S5_L001_R1_001.fastq
Started analysis of 008-F08_S5_L001_R2_001.fastq
Approx 5% complete for 008-F08_S5_L001_R2_001.fastq
Approx 10% complete for 008-F08_S5_L001_R2_001.fastq
Approx 15% complete for 008-F08_S5_L001_R2_001.fastq
Approx 20% complete for 008-F08_S5_L001_R2_001.fastq
Approx 25% complete for 008-F08_S5_L001_R2_001.fastq
Approx 30% complete for 008-F08_S5_L001_R2_001.fastq
Approx 35% complete for 008-F08_S5_L001_R2_001.fastq
Approx 40% complete for 008-F08_S5_L001_R2_001.fastq
Approx 45% complete for 008-F08_S5_L001_R2_001.fastq
Approx 50% complete for 008-F08_S5_L001_R2_001.fastq
Approx 55% complete for 008-F08_S5_L001_R2_001.fastq
Approx 60% complete for 008-F08_S5_L001_R2_001.fastq
Approx 65% complete for 008-F08_S5_L001_R2_001.fastq
Approx 70% complete for 008-F08_S5_L001_R2_001.fastq
Approx 75% complete for 008-F08_S5_L001_R2_001.fastq
Approx 80% complete for 008-F08_S5_L001_R2_001.fastq
Approx 85% complete for 008-F08_S5_L001_R2_001.fastq
Approx 90% complete for 008-F08_S5_L001_R2_001.fastq
Approx 95% complete for 008-F08_S5_L001_R2_001.fastq
Analysis complete for 008-F08_S5_L001_R2_001.fastq
done!
filter qc by IlluQC.pl..
Warning:
	Can not find module 'GD::Graph'
	Graphs for statistics will not be produced.
			OR
	Install GD::Graph module and try again.

Analysis has been started for "008-F08_S5_L001_R1_001.fastq 008-F08_S5_L001_R2_001.fastq N A": Index: 1
1: Checking FASTQ format: File 008-F08_S5_L001_R1_001.fastq...
1: Checking FASTQ format: File 008-F08_S5_L001_R2_001.fastq...
1: Input FASTQ file format: Sanger
1: Processing input files...
1: Number of reads processed: 0/91580 (0%)...
1: Number of reads processed: 91580/91580 (100%)...
1: Analysis completed
1: Printing Statistics...
================================================================
Processing has been finished
Output files are generated in the folder of input files
================================================================
done!
```

