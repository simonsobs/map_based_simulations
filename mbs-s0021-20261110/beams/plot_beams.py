#!/usr/bin/env python3
"""Plot the mbs-0021 SAT beam window functions, with a Gaussian reference.

Reads the IPAC beam tables produced by convert_beams_to_mbs.py (columns ell, B),
one panel per telescope and band, one line per wafer slot, and overplots a
Gaussian beam with the median measured FWHM of that panel.
"""
import argparse
import glob
import os
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def read_ipac(path):
    """Read a two column IPAC table (ell, B) without astropy."""
    ell, beam = [], []
    with open(path) as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("\\") or line.startswith("|"):
                continue
            fields = line.split()
            if len(fields) != 2:
                continue
            try:
                ell.append(float(fields[0]))
                beam.append(float(fields[1]))
            except ValueError:
                continue
    return np.array(ell), np.array(beam)


def gaussian_beam(ell, fwhm_arcmin):
    sigma = np.deg2rad(fwhm_arcmin / 60.0) / np.sqrt(8.0 * np.log(2.0))
    return np.exp(-0.5 * ell * (ell + 1.0) * sigma ** 2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--beam-dir", default=os.path.dirname(os.path.abspath(__file__)),
                        help="directory with beam_*.tbl files")
    parser.add_argument("--summary", default=None,
                        help="beam_summary.csv for the FWHM values (default next to the tables)")
    parser.add_argument("--output", default=None, help="output png")
    args = parser.parse_args()

    summary_path = args.summary or os.path.join(args.beam_dir, "beam_summary.csv")
    fwhm = {}
    if os.path.exists(summary_path):
        with open(summary_path) as handle:
            next(handle)
            for line in handle:
                channel, telescope, band, ws, fwhm_arcmin = line.split(",")[:5]
                fwhm[(telescope, band, ws)] = float(fwhm_arcmin)

    tables = sorted(glob.glob(os.path.join(args.beam_dir, "beam_*.tbl")))
    if not tables:
        raise SystemExit("no beam_*.tbl found in %s" % args.beam_dir)

    groups = {}
    for path in tables:
        match = re.search(r"beam_(satp\d)_(f\d+)_(ws\d)\.tbl$", os.path.basename(path))
        if not match:
            continue
        telescope, band, ws = match.groups()
        groups.setdefault((telescope, band), []).append((ws, path))

    fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True)
    for ax, ((telescope, band), entries) in zip(axes.ravel(), sorted(groups.items())):
        all_fwhm = []
        for ws, path in sorted(entries):
            ell, beam = read_ipac(path)
            ax.plot(ell, beam, lw=1.2, label=ws)
            if (telescope, band, ws) in fwhm:
                all_fwhm.append(fwhm[(telescope, band, ws)])
        if all_fwhm:
            ref_fwhm = float(np.median(all_fwhm))
            ax.plot(ell, gaussian_beam(ell, ref_fwhm), "k--", lw=2.0,
                    label="Gaussian %.1f'" % ref_fwhm)
        ax.set_yscale("log")
        ax.set_ylim(1e-6, 1.5)
        ax.set_xlim(0, 1500)
        ax.set_title("%s %s (20261104_bessel, TF corrected)" % (telescope, band))
        ax.set_ylabel("B(ell)")
        ax.grid(True, which="both", alpha=0.25)
        ax.legend(fontsize=7, ncol=2)
    for ax in axes[-1]:
        ax.set_xlabel("ell")
    fig.suptitle("mbs-0021 SAT beams per wafer slot, normalized at ell=0", fontsize=13)
    fig.tight_layout()
    output = args.output or os.path.join(args.beam_dir, "beams_all.png")
    fig.savefig(output, dpi=150)
    print("wrote", output)


if __name__ == "__main__":
    main()
