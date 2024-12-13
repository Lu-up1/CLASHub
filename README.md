# CLASHub 1.0: Comprehensive miRNA-Target Interaction and Expression Analysis Platform

**CLASHub 1.0** is a user-friendly and powerful platform designed to analyze CLASH (Cross-Linking, Ligation, and Sequencing of Hybrids) data and miRNA expression data. It facilitates comprehensive insights into miRNA-target interactions, miRNA expression dynamics, and their regulatory roles across multiple organisms.

---

## Project Overview

- **Purpose**: CLASHub enables the identification and analysis of miRNA-target interactions and expression profiles using sequencing data.
- **Data Supported**:
  - **Model Organisms**: *Homo sapiens*, *Mus musculus*, *Drosophila melanogaster*, *Caenorhabditis elegans*
  - **Data Types**: CLASH datasets, miRNA-seq, RNA-seq, and differential expression results.

---

## Features

### 1. CLASH Analysis Pipeline (`CLASHub.py`)

The CLASH analysis module processes and identifies miRNA-target interactions using the following workflow:

#### **Step 1: Data Upload and Input**
- Input formats: **Paired-end FASTQ** files or **Cleaned single-end FASTA** files.
- Required inputs:
  - Adapter sequences (5′ and 3′)
  - Target species (e.g., *Homo sapiens*, *Mus musculus*, *Drosophila melanogaster*, *Caenorhabditis elegans*)
  - Output file name
  - Email address for result delivery

#### **Step 2: Data Preprocessing**
- **Adapter Trimming**: Performed using `Cutadapt (v2.10)` to remove adapter sequences.
- **Read Merging**: Paired-end reads are merged using `PEAR (v0.9.6)`.
- **Redundancy Collapse**: Identical sequences are collapsed using `fastx_collapser (v0.0.14)`.
- **UMI Trimming**: Removes unique molecular identifiers (UMIs) to clean up the data.

#### **Step 3: Hybrid Identification**
- Reads are aligned to reference transcripts using `hyb` and `bowtie2 (v2.5.3)`.
- Reference databases include:
  - Ensembl genome assemblies: GRCh38, GRCm39, BDGP6, WBcel235
  - Mature miRNAs from `miRBase (Release 22.1)`
- Binding stability (ΔG) is evaluated using `UNAfold (v3.8)`.

#### **Step 4: Conservation Score Calculation**
- Conservation scores are computed using the custom script `CLASHub.py` (available on GitHub: [CLASHub GitHub](https://github.com/Lu-up1)).
- Scores are derived from UCSC phyloP tracks:
  - *Homo sapiens*: `g38.phyloP100way`
  - *Mus musculus*: `mm39.phyloP35way`
  - *Drosophila melanogaster*: `dm6.phyloP124way`
  - *Caenorhabditis elegans*: `ce11.phyloP135way`

#### **Step 5: Hybrid Quantification and Site Classification**
- Hybrids are classified into binding site types: **8mer, 7mer, 6mer**, and **non-seed matches**.
- Quantification results include miRNA-target abundance.

#### **Step 6: Output Results**
The analysis generates:
- **Detailed Table**:
  - miRNA name, target pairing pattern, gene name/ID, conservation score, free energy, gene type, genomic position, and binding site type.
  - Normalized hybrid abundances across conditions.
- **Summary HTML Report**:
  - Provides key metrics like processed reads, mapped reads, and identified hybrids.

---

### 2. AQ-miRNA-seq Analysis: miRNA Quantification and Isoform Profiling

The AQ-miRNA-seq module processes miRNA sequencing data to quantify total miRNA expression and isoform-specific abundances.

#### **Step 1: Data Upload and Input**
- Input formats:
  - **Paired-End FASTQ** (.gz) files (requires 5′ and 3′ adapter sequences).
  - **Single-End FASTQ** (.gz) files (requires only 3′ adapter sequences).
  - **Cleaned Single-End FASTA** (.gz) files (no adapter trimming required).
- Additional inputs: target species, output file name, and email address.

#### **Step 2: Data Preprocessing**
- **Adapter Trimming**: Uses `Cutadapt (v2.10)` for paired-end and single-end data.
- **Read Merging**: Paired-end reads are merged using `PEAR (v0.9.6)`.
- **Redundancy Collapse**: Removes PCR duplicates with `fastx_collapser`.
- **UMI Trimming**: Cleans up UMIs for FASTQ data.

#### **Step 3: miRNA Identification and Quantification**
- miRNA reads are matched to mature miRNA sequences from `miRBase (Release 22.1)`.
- Expression levels are calculated for:
  - **Total miRNA counts**.
  - **Isoform abundances**, including 3′ end variations.

#### **Step 4: Output Results**
- **Total miRNA Expression Table**: Quantifies miRNA expression levels.
- **Isoform Table**: Details sequence-specific isoform abundances.
- **Summary HTML Report**: Includes metrics on input reads, processed reads, and miRNA mapping rates.

---

### 3. RNA-seq Analysis: Gene Expression and Differential Expression

The RNA-seq module calculates gene expression levels and identifies differentially expressed genes.

#### **Step 1: Data Upload and Input**
- Input format: **Paired-end FASTQ (.gz)** files.
- Required inputs: adapter sequences, target species, output file name, and email address.

#### **Step 2: Data Preprocessing**
- **Adapter Trimming**: Performed using `Cutadapt (v2.10)`.
- **Genome Mapping**: Reads are aligned to reference genomes with `HISAT2 (v2.2.1)`:
  - *Homo sapiens*: GRCh38
  - *Mus musculus*: GRCm39
  - *Drosophila melanogaster*: BDGP6
  - *Caenorhabditis elegans*: WBcel235

#### **Step 3: Gene Expression Quantification**
- Gene expression levels are quantified using `StringTie (v2.2.1)` to produce **TPM**-normalized values.

#### **Step 4: Differential Gene Expression Analysis**
- Raw counts are generated with `prepDE.py3` and analyzed with `DESeq2 (v1.44)` to detect significant fold changes between conditions.

#### **Step 5: Output Results**
- **TPM Table**: Normalized gene expression values.
- **Raw Count Table**: Unprocessed gene-level counts.
- **DESeq2 Results Table**: Includes log2 fold changes, adjusted p-values, and base mean values.
- **Summary HTML Report**: Metrics on reads, trimming, mapping, and expression results.

---

### 4. Cumulative Fraction Curve Analysis: Functional Validation of miRNA Targets

The cumulative fraction curve module evaluates the regulatory effects of miRNAs by comparing fold change distributions between miRNA targets and non-target genes.

#### **Step 1: Data Upload and Input**
- Input: **Differential gene expression CSV** with columns:
  - `GeneName`, `BaseMean`, `log2FoldChange`
- Additional inputs: target species, miRNA name, output file name, and email address.

#### **Step 2: Target Identification**
- **CLASH-Derived Targets**:
  - Conserved targets (high-confidence with phyloP > 0) and all targets.
- **TargetScan-Derived Targets**:
  - Targets downloaded from the `Summary_Counts.txt` file (conserved and non-conserved).

#### **Step 3: Cumulative Fraction Curve Generation**
- Compares fold change distributions of target genes versus non-targets.
- Genes with low expression (BaseMean < threshold) are excluded.

#### **Step 4: Output Results**
- **Cumulative Fraction Curves**: Visualize regulatory trends of miRNA targets.
- **Summary Report**: Key statistics on filtered genes and target classifications.

---

## How to Use the Code

Clone the repository and run the desired analysis pipeline:

```bash
git clone https://github.com/Lu-up1/CLASHub/
