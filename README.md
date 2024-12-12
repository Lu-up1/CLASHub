CLASHub 1.0: Comprehensive miRNA-Target Interaction Analysis Platform

CLASHub 1.0 is a comprehensive and user-friendly platform for analyzing CLASH (Cross-Linking, Ligation, and Sequencing of Hybrids) data. It combines a rich database with advanced tools for data analysis, facilitating the exploration of miRNA-target interactions and their regulatory roles across multiple organisms.

Project Overview
	•	Purpose: CLASHub reveals microRNA (miRNA)–target interactions by utilizing UV cross-linking to covalently bind miRNAs and their target RNAs within the Argonaute protein complex.
	•	Data: The database includes data for four model organisms:
	•	Human (Homo sapiens)
	•	Mouse (Mus musculus)
	•	Drosophila melanogaster
	•	Caenorhabditis elegans
	•	Samples: Data include wild-type, non-targeting sgRNA controls, and ZSWIM8 knockout samples, providing insights into Target-Directed miRNA Degradation (TDMD).

Features

1. CLASH Analysis Pipeline (CLASHub.py)

The core script CLASHub.py processes and analyzes CLASH data through the following steps:

Step 1: Data Upload and Input
	•	Input Formats: Paired-end FASTQ files or single-end FASTA files.
	•	Minimal user-provided information:
	•	Adapter sequences (5’ and 3’)
	•	Target species
	•	Output file name
	•	Email address for notifications

Step 2: Data Preprocessing
	•	Adapter Trimming: Removed using cutadapt (v2.10) (Martin, 2011).
	•	Read Merging: Performed with PEAR (v0.9.6) (Zhang et al., 2014).
	•	Redundancy Collapse: Redundant reads are collapsed using fastx_collapser.
	•	UMI Trimming: Unique Molecular Identifiers are trimmed to produce clean data.


Step 3: Hybrid Identification
	•	Reads are aligned to reference transcripts using hyb (Travis et al., 2014) and bowtie2 (v2.5.3).
	•	Reference databases include Ensembl genome assemblies (Harrison et al., 2024) and mature miRNAs from miRBase (Release 22.1).
	•	Binding stability (free energy, ΔG) is assessed using UNAfold (v3.8) (Markham and Zuker, 2008).

Step 4: Conservation Score Calculation
	•	At this step, the CLASHub.py script is utilized to calculate the conservation socre of specific miRNA binding sites within target genes. The conservation scores are derived from UCSC phyloP tracks.
	•	Conservation is assessed using UCSC phyloP tracks (Perez et al., 2024):
	•	Human: g38.phyloP100way
	•	Mouse: mm39.phyloP35way
	•	Drosophila: dm6.phyloP124way
	•	C. elegans: ce11.phyloP135way

Step 5: Hybrid Quantification and Site Type Analysis
	•	The CLASHub.py script integrates the processed results to quantify identified miRNA-target hybrids.
	•	Hybrids are classified into site types: Offset 6mer, 6mer, 7mer-A1, 7mer-m8, and 8mer.
	•	Results are summarized into a comprehensive table for downstream analysis.

Step 6: Output Results

The CLASHub.py script produces the final output in the form of a detailed table and HTML report. The output includes:
	•	6.1 miRNA Name (from miRBase)
	•	6.2 Pairing Pattern (miRNA sequence, target sequence, and base pairing relationships)
	•	6.3 Gene Name (from Ensembl)
	•	6.4 Gene ID (from Ensembl)
	•	6.5 Conservation Score (calculated using UCSC phyloP tracks)
	•	6.6 Free Energy (ΔG via UNAfold)
	•	6.7 Gene Type (e.g., mRNA, lncRNA)
	•	6.8 Element Region (e.g., CDS, 5’UTR, or 3’UTR)
	•	6.9 Genomic Position
	•	6.10 Binding Site Type (e.g., 8mer, 7mer, or non-seed match)
	•	6.11 Number of Datasets with Hybrid Occurrence (wild-type, control, ZSWIM8 knockout)
	•	6.12 Normalized Hybrid Abundance (quantified across wild-type, control, and ZSWIM8 knockout datasets).

2. MicroRNA Expression Analysis

CLASHub can calculate miRNA expression levels across different samples, enabling insights into miRNA abundance in wild-type, control, and knockout datasets.

3. Cumulative Fraction Curve Analysis

The cumulative fraction curve tool allows researchers to visualize the distribution of miRNA binding and its effects on target gene regulation.

How to Use the Code
	•	Clone or download this repository:

git clone https://github.com/your-username/CLASHub.git

Outputs
	•	A detailed HTML report summarizing results.
	•	A comprehensive table containing miRNA-target interaction details, binding site classification, and quantification results.

License

This project is open and free to use under the MIT License.

Acknowledgments
	•	Developed as part of the CLASH Hub Project at the University of Florida.
	•	Data resources: Ensembl, miRBase, and UCSC Genome Browser.
	•	Tools used: cutadapt, PEAR, bowtie2, UNAfold, and phyloP tracks.

Contact

For questions or feedback, please contact:
Lu Li
luli1@ufl.edu

