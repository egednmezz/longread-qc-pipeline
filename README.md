# Case Study: Mini-Bioinformatics Pipeline & Reporting

A reproducible **Long-read QC pipeline** built with **Nextflow + Conda**.

---

##  Project Structure

```
longread-qc-pipeline/
├── main.nf                    # Nextflow pipeline 
├── nextflow.config            # Pipeline configuration & profiles
├── environment.yml            # Conda environment definition
├── data/
│   └── barcode77.fastq.gz     # Input: raw FASTQ file 
├── scripts/
│   ├── calculate_metrics.py   # Per-read GC, length, quality → CSV
│   └── visualize.py           # Distribution plots from CSV
├── results/                   # Auto-generated outputs
│   ├── quality_report/        # Quality control summary statistics
│   ├── read_statistics/       # Per-read GC content, length, quality (CSV)
│   └── plots/                 # PNG distribution plots
└── README.md
```

---

##  Pipeline Steps

```
<input.fastq.gz>
        │
        ├──────────────────────────┐
        ▼                          ▼
  [1] NanoPlot QC         [2] calculate_metrics.py
        │                          │
        ▼                          ▼
quality_report/             read_statistics/
nanostat_report.txt            statistics.csv
                                   │
                                   ▼
                          [3] visualize.py
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼               ▼
             gc_content.png  read_length.png  mean_quality.png
```
> **Note:** Pipeline accepts any FASTQ file as input.
> `barcode77.fastq.gz` is used as the example dataset in this project.

---

##  Installation

### Prerequisites
- [Conda](https://docs.conda.io/en/latest/miniconda.html) 
- [Nextflow](https://www.nextflow.io/) ≥ 23.0

### 1. Clone the repository
```bash
git clone https://github.com/egednmezz/longread-qc-pipeline.git
cd longread-qc-pipeline
```

### 2. Create the Conda environment
```bash
conda env create -f environment.yml
conda activate qc-pipeline
```

### 3. Place your input file
```bash
mkdir data/
cp /path/to/barcode77.fastq.gz data/
```

---

##  Running the Pipeline

### Standard run (local machine)
```bash
nextflow run main.nf \
    --fastq data/barcode77.fastq.gz \
    --outdir results/
```

### Custom output directory
```bash
nextflow run main.nf \
    --fastq data/barcode77.fastq.gz \
    --outdir my_results/ \
    --threads 8
```

### Dry run (check pipeline logic without executing)
```bash
nextflow run main.nf --fastq data/barcode77.fastq.gz -preview
```

### Resume a failed run (Nextflow caches completed steps)
```bash
nextflow run main.nf --fastq data/barcode77.fastq.gz -resume
```

---

## Outputs

| File | Description |
|------|-------------|
| `results/quality_report/nanostat_report.txt` | NanoStat QC statistics summary  
| `results/read_statistics/statistics.csv`     | Per-read GC content percentage, read length, mean read quality score 
| `results/plots/gc_content.png`               | GC content distribution 
| `results/plots/read_length.png`              | Read length distribution (log scale) 
| `results/plots/mean_quality.png`             | Mean Phred quality score distribution 
| `results/pipeline_report.html`               | Nextflow execution report 
| `results/pipeline_timeline.html`             | Step-by-step timeline 
| `results/pipeline_dag.html`                  | Visual graph of pipeline step dependencies
---

## Reporting

> Dear Professor Kılıç,
>
> I have completed the quality control analysis of the raw sequencing data (barcode77.fastq.gz) you provided.
> Here is a summary of what was done and what the results indicate.
>
> 
> I ran the raw sequencing file through a reproducible bioinformatics pipeline. The pipeline checked the overall
> quality of the data using NanoStat tool and then calculated GC content, read length, mean read quality scores for each
> of the 81,011 individual sequencing reads, saving these metrics as a CSV file. The pipeline also generated an overall quality summary of the dataset.
> These three metrics were then visualized as histogram distributions, which I have interpreted below.

> **What the plots show:**
> - **GC Content:** The distribution is centered around 40–60%, which is the expected. The vast majority of reads have
>   a GC content centered around 53%. This symmetric bell-shaped distribution suggest the sample is clean and consistent, with no signs
>   of serious contamination or technical issues.
>   
> - **Read Length:** The read length distribution shows a median of 547 bp and a mean of 1,038 bp, with an N50 value of 1,761 bp.
>   These values are considerably lower than what is typically expected from long read sequencing technology.The large gap between the mean and median
>   indicates that while a small number of very long reads exist in the dataset, the majority of reads are relatively short.
>
> - **Mean Read Quality Score:** The quality distribution displays a bimodal profile with a mean of 17.90 and a median of 17.31.
>   Two peaks are observed around Q7 and Q11, representing a subpopulation of lower-quality reads with a higher error rate.
>   This is followed by a broad plateau between Q15 and Q30, indicating a second population of higher-quality reads suitable for alignment and variant calling.
>    While the median quality is above the Q10 threshold, approximately 51.4% of reads fall below Q10 at the base level according to the NanoStat summary. 
>
> **Recommendation:** Based on the quality control analysis, proceeding directly to alignment is not recommended without prior filtering.
> Due to the high frequency of low-quality reads (Q<10), a pre-processing step involving quality filtering (Q>12) and length filtering (>1kb) is mandatory.
> After filtering,reassess the remaining data volume to ensure sufficient coverage for the target organism. If the filtered dataset retains enough reads for adequate genome coverage, 
> alignment is recommended as the next step.
> 
> Please let me know if you have any questions.
>
> Best regards,
> Ege Dönmez

---

## Reproducibility

This pipeline is fully reproducible:
- All software versions are pinned in `environment.yml`
- Nextflow's `-resume` flag reuses cached results
- The DAG diagram is auto-generated at `results/pipeline_dag.html`
