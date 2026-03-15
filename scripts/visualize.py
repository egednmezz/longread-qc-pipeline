#!/usr/bin/env python3
"""
------------
Reads the metrics CSV produced by calculate_metrics.py and generates
three publication-quality distribution plots:
  1. GC Content distribution
  2. Read Length distribution
  3. Mean Read Quality Score distribution

Usage:
    python visualize.py <metrics.csv> <output_plots_dir/>
"""

import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns


# Global plot style 
sns.set_theme(style="whitegrid", context="notebook", font_scale=1.2)
PALETTE = {
    "gc_content":   "#2196F3",   # blue
    "read_length":  "#4CAF50",   # green
    "mean_quality": "#9C27B0",   # purple
}


# Plotting functions 

def plot_gc_content(df: pd.DataFrame, out_dir: Path) -> None:
    """Histogram + KDE for GC content percentage."""
    fig, ax = plt.subplots(figsize=(9, 5))

    sns.histplot(
        df["gc_content"], bins=50, kde=True,
        color=PALETTE["gc_content"], alpha=0.75, ax=ax,
    )

    mean_val   = df["gc_content"].mean()
    median_val = df["gc_content"].median()

    ax.axvline(mean_val,   color="red",    linestyle="--", linewidth=1.8,
               label=f"Mean:   {mean_val:.2f}%")
    ax.axvline(median_val, color="orange", linestyle=":",  linewidth=1.8,
               label=f"Median: {median_val:.2f}%")

    ax.set_title("GC Content Distribution", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("GC Content (%)")
    ax.set_ylabel("Number of Reads")
    ax.legend(framealpha=0.9)

    plt.tight_layout()
    out_path = out_dir / "gc_content.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"[INFO] Saved: {out_path}")


def plot_read_length(df: pd.DataFrame, out_dir: Path) -> None:
    """
    Histogram + KDE for read lengths.
    Uses log-scale on x-axis because ONT read lengths span orders of magnitude.
    """
    fig, ax = plt.subplots(figsize=(9, 5))

    # Log-binned histogram is cleaner for long-read data
    sns.histplot(
        df["read_length"], bins=60, kde=False,
        color=PALETTE["read_length"], alpha=0.75, ax=ax, log_scale=(True, False),
    )

    mean_val   = df["read_length"].mean()
    median_val = df["read_length"].median()

    ax.axvline(mean_val,   color="red",    linestyle="--", linewidth=1.8,
               label=f"Mean:   {mean_val:,.0f} bp")
    ax.axvline(median_val, color="orange", linestyle=":",  linewidth=1.8,
               label=f"Median: {median_val:,.0f} bp")

    ax.set_title("Read Length Distribution", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("Read Length (bp, log scale)")
    ax.set_ylabel("Number of Reads")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.legend(framealpha=0.9)

    plt.tight_layout()
    out_path = out_dir / "read_length.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved: {out_path}")


def plot_mean_quality(df: pd.DataFrame, out_dir: Path) -> None:
    """Histogram + KDE for mean per-read Phred quality scores."""
    fig, ax = plt.subplots(figsize=(9, 5))

    sns.histplot(
        df["mean_quality"], bins=50, kde=True,
        color=PALETTE["mean_quality"], alpha=0.75, ax=ax,
    )

    mean_val   = df["mean_quality"].mean()
    median_val = df["mean_quality"].median()

    ax.axvline(mean_val,   color="red",    linestyle="--", linewidth=1.8,
               label=f"Mean:   {mean_val:.2f}")
    ax.axvline(median_val, color="orange", linestyle=":",  linewidth=1.8,
               label=f"Median: {median_val:.2f}")

    # Reference lines for common quality thresholds
    ax.axvline(8,  color="gray", linestyle="-", linewidth=1, alpha=0.5, label="Q8 threshold")
    ax.axvline(10, color="gray", linestyle="-", linewidth=1, alpha=0.8, label="Q10 threshold")

    ax.set_title("Mean Read Quality Score Distribution", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("Mean Phred Quality Score")
    ax.set_ylabel("Number of Reads")
    ax.legend(framealpha=0.9)

    plt.tight_layout()
    out_path = out_dir / "mean_quality.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"[INFO] Saved: {out_path}")


def print_summary(df: pd.DataFrame) -> None:
    """Print formatted summary statistics table."""
    metrics = {
        "gc_content":   "GC Content (%)",
        "read_length":  "Read Length (bp)",
        "mean_quality": "Mean Quality (Phred)",
    }
    print("── Summary Statistics ──────────────────────────────────────")
    print(f"  {'Metric':<25} {'Mean':>10} {'Median':>10} {'Std':>10}")
    print(f"  {'-'*55}")
    for col, label in metrics.items():
        print(
            f"  {label:<25}"
            f" {df[col].mean():>10.2f}"
            f" {df[col].median():>10.2f}"
            f" {df[col].std():>10.2f}"
        )
    print(f"  Total reads: {len(df):,}")
    print("────────────────────────────────────────────────────────────")


#  Main 

def main():
    if len(sys.argv) != 3:
        print("Usage: python visualize.py <metrics.csv> <output_plots_dir/>")
        sys.exit(1)

    metrics_path = sys.argv[1]
    plots_dir    = Path(sys.argv[2])
    plots_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Loading metrics from: {metrics_path}")
    df = pd.read_csv(metrics_path)
    print(f"Loaded {len(df):,} reads.")

    print_summary(df)

    plot_gc_content(df, plots_dir)
    plot_read_length(df, plots_dir)
    plot_mean_quality(df, plots_dir)

    print("All plots generated successfully.")


if __name__ == "__main__":
    main()
