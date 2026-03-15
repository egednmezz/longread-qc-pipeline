#!/usr/bin/env python3

"""
calculate_metrics.py
Per-read GC content, read length, and mean quality score from a FASTQ file.

Usage:
    python calculate_metrics.py <input.fastq.gz> <output.csv>
"""

import gzip
import sys
from Bio import SeqIO
import pandas as pd

# Opens .gz files in text mode
def open_fastq(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path, "r")

# Calculates GC content percentage
def calc_gc(seq):
    return round(sum(1 for b in seq if b in "GCgc") / len(seq) * 100, 4) if seq else 0

# Averages the Phred quality scores across all bases in a read
def calc_mean_quality(quals):
    return round(sum(quals) / len(quals), 4) if quals else 0

# Parses the FASTQ file and computes metrics for each read, returning a DataFrame
def parse_fastq(path):
    records = []
    with open_fastq(path) as fh:
        for rec in SeqIO.parse(fh, "fastq"):
            records.append({
                "read_id":      rec.id,
                "read_length":  len(rec.seq),
                "gc_content":   calc_gc(str(rec.seq)),
                "mean_quality": calc_mean_quality(rec.letter_annotations["phred_quality"]),
            })
    return pd.DataFrame(records)

# Prints mean and median for each metric as a quick sanity check
def print_summary(df):
    print("\n── Summary Statistics ───────")
    for col in ["gc_content", "read_length", "mean_quality"]:
        print(f"  {col:<15}  mean={df[col].mean():.2f}  median={df[col].median():.2f}")
    print(f"  Total reads: {len(df):,}\n")


if __name__ == "__main__":

#Ensure the user provided exactly two arguments: input file and output file
    if len(sys.argv) != 3:
        print("Usage: python calculate_metrics.py <input.fastq.gz> <output.csv>")
        sys.exit(1)

    input_path, output_path = sys.argv[1], sys.argv[2]
#Parse the FASTQ file and compute per-read metrics
    print(f"[INFO] Reading: {input_path}")
    df = parse_fastq(input_path)
    print_summary(df)

# Save results to CSV for downstream visualization    
    df.to_csv(output_path, index=False)
    print(f"[INFO] Saved: {output_path}")
