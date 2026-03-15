# Case Study: Mini-Bioinformatics Pipeline & Reporting

A reproducible **Long-read QC pipeline** built with **Nextflow + Conda**.

---

##  Project Structure

```
mini-bioinfo-pipeline/
├── main.nf                    # Nextflow pipeline (main entry point)
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
  [1] NanoStat QC          [2] calculate_metrics.py
        │                          │
        ▼                          ▼
  qc/nanostat_report.txt    metrics/metrics.csv
                                   │
                                   ▼
                          [3] visualize.py
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼               ▼
             gc_content.png  read_length.png  mean_quality.png
```
> **Note:** Pipeline accepts any ONT FASTQ file as input.
> `barcode77.fastq.gz` is used as the example dataset in this project.

---

##  Installation

### Prerequisites
- [Conda](https://docs.conda.io/en/latest/miniconda.html) 
- [Nextflow](https://www.nextflow.io/) ≥ 23.0

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/mini-bioinfo-pipeline.git
cd mini-bioinfo-pipeline
```

### 2. Create the Conda environment
```bash
conda env create -f environment.yml
conda activate qc-pipeline
```

### 3. Place your input file
```bash
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
| `results/read_statistics/statistics.csv`     | Per-read GC content, length, quality 
| `results/plots/gc_content.png`               | GC content distribution 
| `results/plots/read_length.png`              | Read length distribution (log scale) 
| `results/plots/mean_quality.png`             | Mean Phred quality score distribution 
| `results/pipeline_report.html`               | Nextflow execution report 
| `results/pipeline_timeline.html`             | Step-by-step timeline 
| `results/pipeline_dag.html`                  | Visual graph of pipeline step dependencies
---

## Email to Professor Kılıç

> Dear Professor Kılıç,
>
> I have completed the quality control analysis of the Oxford Nanopore sequencing data
> (barcode77.fastq.gz) from your lab's recent run. Here is a plain-language summary
> of what was done and what the results indicate.
>
> **What I analyzed:**
> I processed the raw sequencing file through a reproducible bioinformatics pipeline.
> For each sequencing read, I calculated three key metrics: (1) GC content — the
> percentage of G and C bases in the sequence, (2) read length — how many base pairs
> each read contains, and (3) mean quality score — a measure of how confident the
> sequencer was in each base call.
>
> **What the plots show:**
> - **GC Content:** The distribution is centered around 40–60%, which is the expected
>   range for most organisms. A very skewed distribution would indicate contamination
>   or adapter issues, so this looks normal.
> - **Read Length:** Oxford Nanopore typically produces reads spanning a wide range —
>   from a few hundred to tens of thousands of base pairs. The plot (shown on a log
>   scale) reveals the spread of your library's fragment sizes.
> - **Mean Quality Score:** Phred quality scores above Q8 mean less than 1 error in
>   every 6 bases. A score of Q10 means 90% accuracy per base. If your data's median
>   quality is above Q8, it is generally considered usable for alignment.
>
> **Recommendation:**
> If the median quality score is ≥ Q8 and the median read length is ≥ 1,000 bp,
> I recommend proceeding to the alignment step using a tool like minimap2, which is
> specifically optimized for long Nanopore reads. I am happy to set this up for you.
>
> Please let me know if you have any questions.
>
> Best regards,
> Bioinformatics Intern

---

## Reproducibility

This pipeline is fully reproducible:
- All software versions are pinned in `environment.yml`
- Nextflow's `-resume` flag reuses cached results
- The DAG diagram is auto-generated at `results/pipeline_dag.html`
