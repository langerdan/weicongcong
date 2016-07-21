# GATK

> ***Version:*** v0.01a
>
> ***Author:*** codeunsolved@gmail.com
>
> ***Created:*** July 15 2016



## 1. Build the index

\- *Run once* -

###1.1 BWA index

```shell
bwa index /path/to/ref.fasta
```



## 2. Aligning with BWA-MEM

### 2.1 Paired-end(PE) mode

```shell
bwa mem -t 4 -M /path/to/ref_index_prefix /path/to/r1.fastq /path/to/r2.fastq >/path/to/.sam
```

> **-t** *INT*	Number of threads [1]
>
> **-M**		Mark shorter split hits as secondary (for Picard compatibility)
>
> **-R** *STR*	Complete read group header line. ’\t’ can be used in STR and will be converted to a TAB in the output SAM. The read group ID will be attached to every read in the output. An example is ’@RG\tID:foo\tSM:bar’. [null]

*from [Manual Reference Pages  - bwa (1)](http://bio-bwa.sourceforge.net/bwa.shtml)*



## 3. Handle SAM

### 3.1 SAM > BAM

```shell
samtools view -b /path/to/.sam -o /path/to/.bam
```

```shell
samtools view -bhS /path/to/.sam >/path/to/.bam
```

> **-b**		output BAM
>
> **-o** *FILE* 	output file name [stdout]
>
> **-h** 		include header in SAM output
>
> **-S** 		ignored (input format is auto-detected)



### 3.2 Sort BAM

```shell
samtools sort /path/to/.bam >/path/to/.sort.bam
```



### 3.3 Index BAM

#### 3.3.1 by samtools

```shell
samtools index /path/to/.sort.bam >/path/to/.sort.bam.bai
```





