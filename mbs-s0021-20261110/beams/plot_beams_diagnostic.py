#!/usr/bin/env python3
"""Diagnostic: raw 20261104_bessel window function vs the mbs adopted beam.

The Bessel fit behind the product is only meaningful up to `lmax`; beyond it the
stored B(ell) oscillates and floors at about 1e-3 instead of decaying. This plot
shows the raw product (dashed) and the adopted beam with a Gaussian tail matched
at lmax (solid) for representative channels.

Needs beams_raw.npz (not committed), produced by dumping TF_corrected_B_l from
the per-wafer npz on Tiger3.
"""
import argparse
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plot_beams import read_ipac

CHANNELS = ["satp1_f090_ws0", "satp1_f150_ws0", "satp3_f090_ws3"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--beam-dir", default=os.path.dirname(os.path.abspath(__file__)))
    parser.add_argument("--raw", required=True, help="beams_raw.npz with ell and raw B(ell) per channel")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    raw = np.load(args.raw)
    ell_raw = raw["ell"]
    fig, axes = plt.subplots(1, len(CHANNELS), figsize=(15, 4.6), sharey=True)
    for ax, channel in zip(axes, CHANNELS):
        ax.plot(ell_raw, raw[channel], "--", color="tab:red", lw=1.3, label="raw product")
        table = os.path.join(args.beam_dir, "beam_%s.tbl" % channel)
        ell, beam = read_ipac(table)
        ax.plot(ell, beam, "-", color="tab:blue", lw=1.8, label="adopted (Gaussian tail)")
        ax.set_yscale("log")
        ax.set_ylim(1e-9, 1.5)
        ax.set_xlim(0, 1500)
        ax.set_title(channel)
        ax.set_xlabel("ell")
        ax.grid(True, which="both", alpha=0.25)
        ax.legend(fontsize=8)
    axes[0].set_ylabel("B(ell)")
    fig.suptitle("SO 20261104_bessel: Bessel fit is valid only up to lmax", fontsize=13)
    fig.tight_layout()
    output = args.output or os.path.join(args.beam_dir, "beams_raw_vs_adopted.png")
    fig.savefig(output, dpi=150)
    print("wrote", output)


if __name__ == "__main__":
    main()
