#!/usr/bin/env python3
"""Convert SO SAT per-wafer beam npz products to mbs IPAC beam tables.

The 20261104_bessel product stores, per telescope/band/wafer-slot:
  TF_corrected_B_l        beam window function B(ell), ell = 0..1999
  TF_corrected_omega_b    beam solid angle, TF corrected
mapsims passes the custom beam to pysm as beam_window, which multiplies the
alms, so the table must hold the amplitude beam
B(ell) = TF_corrected_B_l * (2 pi / TF_corrected_omega_b),
renormalized to 1 at ell = 0 (the product itself is about 0.3 percent above 1).

Output: one IPAC table per channel with columns ell and B, plus a CSV summary.
"""
import argparse
import csv
import glob
import os

import numpy as np

PREFIX = "20261104_bessel_ISO_beam_fitting_results_"


def parse_name(path):
    stem = os.path.basename(path)[len(PREFIX):-len(".npz")]
    telescope, ws, band = stem.split("_")
    return telescope, band, ws


def window_function(data):
    b_l = np.asarray(data["TF_corrected_B_l"], dtype=float)
    omega = float(data["TF_corrected_omega_b"])
    beam = b_l * (2.0 * np.pi / omega)
    # the product stores B(ell) with a global minus sign (transform convention)
    if beam[0] < 0:
        beam = -beam
    raw_zero = float(beam[0])
    return beam / raw_zero, raw_zero, omega


def write_ipac(path, ell, window, telescope, band, ws):
    with open(path, "w") as handle:
        handle.write("\\ Text file in IPAC table format, read with astropy\n")
        handle.write(
            "\\ mbs-0021 SAT beam from SO 20261104_bessel, "
            "%s %s %s, TF corrected, normalized at ell=0\n" % (telescope, band, ws)
        )
        handle.write("|    ell|                     B|\n")
        handle.write("| double|                double|\n")
        handle.write("|       |                      |\n")
        handle.write("|   null|                  null|\n")
        for e, value in zip(ell, window):
            handle.write("%9.1f %21.14f\n" % (e, value))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", required=True, help="directory with the per-wafer npz files")
    parser.add_argument("--output-dir", required=True, help="directory for the IPAC tables")
    parser.add_argument("--dump-arrays", default=None, help="optional npz with ell and B(ell) per channel")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    files = sorted(glob.glob(os.path.join(args.input_dir, PREFIX + "*.npz")))
    if not files:
        raise SystemExit("no per-wafer npz found in %s" % args.input_dir)

    rows = []
    arrays = {}
    ell = None
    for path in files:
        telescope, band, ws = parse_name(path)
        channel = "%s_%s_%s" % (telescope, band, ws)
        with np.load(path, allow_pickle=False) as data:
            window, raw_zero, omega = window_function(data)
            fwhm = float(data["TF_corrected_fwhm"])
            lmax = int(data["lmax"])
        if ell is None:
            ell = np.arange(window.size, dtype=float)
        elif window.size != ell.size:
            raise SystemExit("inconsistent ell size in %s" % path)
        out_name = "beam_%s.tbl" % channel
        write_ipac(os.path.join(args.output_dir, out_name), ell, window, telescope, band, ws)
        arrays[channel] = window
        rows.append(
            {
                "channel": channel,
                "telescope": telescope,
                "band": band,
                "ws": ws,
                "fwhm_arcmin": "%.4f" % fwhm,
                "omega_sr": "%.6e" % omega,
                "raw_B0": "%.6f" % raw_zero,
                "lmax": lmax,
                "B_ell_100": "%.6f" % window[100],
                "B_ell_300": "%.6f" % window[300],
                "B_ell_1000": "%.6f" % window[1000],
                "file": out_name,
            }
        )

    summary = os.path.join(args.output_dir, "beam_summary.csv")
    with open(summary, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print("wrote %d beam tables and %s" % (len(rows), summary))

    if args.dump_arrays:
        np.savez_compressed(args.dump_arrays, ell=ell, **arrays)
        print("wrote", args.dump_arrays)


if __name__ == "__main__":
    main()
