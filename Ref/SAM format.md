# SAM format

> *from [SAM V1](https://samtools.github.io/hts-specs/SAMv1.pdf)*

## 1. The Header section



## 2. The Alignment section 

### 2.1 Mandatory fields

>  ![the mandatory fileds in the SAM format](/Users/codeunsolved/Desktop/屏幕快照 2016-07-22 下午1.27.02.png)



Alignment section 示例：

```
02961:56:000000000-AMPHB:1:1101:15303:1347     99      chr17   41197497        60      150M    =       41197623        277     CAAGGGAGACTTCAAGCAGAAAATCTTTAAGGGACCCTTGCATAGCCAGAAGTCCTTTTCAGGCTGATGTACATAAAATATTTAGTAGCCAGGACAGTAGAAGGACTGAAGAGTGAGAGGAGCTCCCAGGGCCTGGAAAGGCCACTTTGT  CCCCCCCCCCFFGGGGGGGGGGHHHGHHHFHFFHGGGHHHHHHHFHHHHHHHHHHHHHHHHHHHHHHHHGHHHHHHHHHHHHHHHHHHHHHHHGHFGHHHHHHHHHHHHGHHHHHEHGHGHGGHHHGHHGGGGGGHHHHGHHHHGHHHHH  NM:i:0  MD:Z:150        AS:i:150        XS:i:109
```



>1. **QNAME**: Query template NAME. Reads/segments having identical QNAME are regarded to come from the same template. A QNAME ‘*’ indicates the information is unavailable. In a SAM file, a read may occupy multiple alignment lines, when its alignment is chimeric or when multiple mappings are given.
>2. **FLAG**: Combination of bitwise FLAGs. Each bit is explained in the following table.
>   ​
>    ![Combination of bitwise FLAGs](/Users/codeunsolved/Desktop/屏幕快照 2016-07-22 下午1.49.33.png)
>   - For each read/contig in a SAM file, it is required that one and only one line associated with theread satisfies ‘FLAG & 0x900 == 0’. This line is called the primary line of the read.
>   - Bit 0x100 marks the alignment not to be used in certain analyses when the tools in use are aware of this bit. It is typically used to flag alternative mappings when multiple mappings are presented in a SAM.
>   - Bit 0x800 indicates that the corresponding alignment line is part of a chimeric alignment. A line flagged with 0x800 is called as a supplementary line.
>   - Bit 0x4 is the only reliable place to tell whether the read is unmapped. If 0x4 is set, no assumptions can be made about RNAME, POS, CIGAR, MAPQ, and bits 0x2, 0x100, and 0x800.
>   - Bit 0x10 indicates whether SEQ has been reverse complemented and QUAL reversed. When bit 0x4 is unset, this corresponds to the strand to which the segment has been mapped. When 0x4 is set, this indicates÷ whether the unmapped read is stored in its original orientation as it came off the sequencing machine.
>   - If 0x40 and 0x80 are both set, the read is part of a linear template, but it is neither the first nor the last read. If both 0x40 and 0x80 are unset, the index of the read in the template is unknown. This may happen for a non-linear template or the index is lost in data processing.
>   - If 0x1 is unset, no assumptions can be made about 0x2, 0x8, 0x20, 0x40 and 0x80
>   - Bits that are not listed in the table are reserved for future use. They should not be set when writing and should be ignored on reading by current software.

