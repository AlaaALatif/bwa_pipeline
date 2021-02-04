# align reads
```bash
bwa mem -t {threads} {ref} {forward_reads} {reverse_reads} | samtools view -Sb | samtools sort -T {sample_name}.align -o {tmp}
```
# merge libraries
```bash
samtools merge {output_bam} {input_bam}(s)
samtools sort -T sample_name.merge -o {sample_with_host.sorted.bam} {sample_name.bam}
samtools view -b -F 4 {sample_with_host.sorted.bam} > {sample_name.sorted.bam}
cat {forward_reads} > {forward_merged_fastq}
cat {reverse_reads} > {reverse_merged_fastq}
```
# extract barcode reads
```bash
bwa mem {insert_reference} {forward_merged_fastq} {reverse_merged_fastq} | samtools view -F 4 -b > {sample_barcode.bam}
samtools sort -o {sample_barcode.coord.bam} {sample_barcode.bam}
samtools index {sample_barcode.coord.bam}
samtools depth -aa -d 0 {sample_barcode.coord.bam} > {sample_barcode.depth}
samtools sort -n -o {sample_barcode.name.bam} {sample_barcode.bam}
samtools fastq -1 {forward_barcodes.fastq.gz} -2 {reverse_barcodes.fastq.gz} -0 /dev/null -s /dev/null {sample_barcode.name.bam}
```
# demultiplex barcodes 
```bash
cutadapt -O 15 -e 0.1 -g file:{ref_forward_barcodes_combined.fa} -G file:{ref_reverse_barcodes_combined.fa} -o {output_dir}/{{name1}}-{{name2}}.1.fastq.gz -p {params.barcode_dir}/{{name1}}-{{name2}}.2.fastq.gz {forward_barcodes.fastq.gz} {reverse_barcodes.fastq.gz} > {log}
echo -e "forward_barcode\treverse_barcode\tpaired_read_count" > {barcodes.tsv}
find {output_dir} -name "*.fastq.gz" | sort | xargs -n 2 bash -c 'n1=$(basename $0 | sed "s/.1.fastq.gz//g" | sed "s/-/\\t/g");echo -e "${{n1}}\t"$(($(zcat $0 | wc -l)/4))' | sort -k 1 >> {output}
```
# trim reads
```bash
ivar trim -e -i sample_name.sorted.bam -b primers.bed -p sample_name.trimmed.tmpbam > trim.log
samtools sort -T sample_name.trim -o sample_name.trimmed.sorted.bam sample_name.trimmed.tmpbam
samtools index sample_name.trimmed.sorted.bam
```
# call consensus
```bash
samtools mpileup -aa -A -Q 0 -d 0 sample_name.trimmed.sorted.bam | ivar consensus -p sample_name.fa -m 10 -n N -t 0.5 > consensus.log
```
# enumerate within-host variants
```bash
samtools mpileup -A -aa -d 0 -Q --reference {ref} sample_name.trimmed.sorted.bam | ivar variants -r {ref_fasta} -g {ref_gff} -p sample_variants -m 10
```


