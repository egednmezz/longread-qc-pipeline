#!/usr/bin/env nextflow
/*
================================================================================
  Case Study: Mini-Bioinformatics Pipeline & Reporting 
================================================================================

  Pipeline steps:
    1. NANOSTAT_QC      → Quality control using NanoStat
    2. CALC_METRICS     → Per-read GC content, length, quality (Python + Biopython)
    3. VISUALIZE        → Distribution plots (Python + matplotlib/seaborn)

  Usage:
    nextflow run main.nf --fastq data/barcode77.fastq.gz --outdir results/
================================================================================
*/

nextflow.enable.dsl = 2


// Step 1: Quality control with NanoStat tool

process NANOSTAT_QC {
    publishDir "${params.outdir}/quality_report", mode: "copy"
   
    input:  path fastq
    output: path "nanostat_report.txt"

    script:
    """
    NanoStat --fastq ${fastq} --threads ${params.threads} > nanostat_report.txt
    """
}


// Step 2: Calculate per-read metrics (GC content, read length, mean read quality scores)
process CALC_METRICS {
    publishDir "${params.outdir}/read_statistics", mode: "copy"

    input:  path fastq
    output: path "statistics.csv", emit: csv

    script:
    """
    python ${projectDir}/scripts/calculate_metrics.py ${fastq} statistics.csv
    """
}


// Step 3: Visualize metrics with Python 
process VISUALIZE {
    publishDir "${params.outdir}/plots", mode: "copy"
    
    input:  path statistics_csv
    output: path "*.png"

    script:
    """
    python ${projectDir}/scripts/visualize.py ${statistics_csv} ./
    """
}


// Workflow: steps 1 and 2 run in parallel, step 3 waits for step 2

workflow {
    // Check if the required parameter is provided
    if (!params.fastq) {
        error """
        ========================================
        ERROR: --fastq parameter is not specified!
        Usage:
          nextflow run pipeline.nf --fastq <sample.fastq.gz>
        Example:
          nextflow run pipeline.nf --fastq data/barcode77.fastq.gz
        ========================================
        """
    }

    log.info """
    Quality Control (QC) Pipeline
    =============================
    Input  : ${params.fastq}
    Output : ${params.outdir}
    """.stripIndent()

    fastq_ch = Channel.fromPath(params.fastq, checkIfExists: true)

    NANOSTAT_QC(fastq_ch)
    CALC_METRICS(fastq_ch)
    VISUALIZE(CALC_METRICS.out.csv)
}


workflow.onComplete {
    log.info "Pipeline ${workflow.success ? 'completed successfully' : 'FAILED'} in ${workflow.duration}"
    }