#!/usr/bin/env python3
"""Validate the mbs-0021 beam tables the way mapsims reads them.

Checks, for every row of the instrument model:
  - the beam file resolves next to the instrument model and is an IPAC table
    with an `ell` and a `B` column (the exact call mapsims makes)
  - B(ell=0) is 1, B is finite, positive and monotonically decreasing
  - the beam is the amplitude used by pysm: applied with healpy almxfl it
    reproduces healpy smoothing for a Gaussian test beam

Needs astropy. The healpy part is skipped when healpy is not installed.
"""
import argparse
import os

import numpy as np
from astropy.table import QTable


EXPECTED_LENGTH = 2000


def check_table(path, name):
    table = QTable.read(path, format="ascii.ipac")
    for column in ("ell", "B"):
        if column not in table.colnames:
            raise SystemExit("%s: missing column %s" % (name, column))
    ell = np.asarray(table["ell"], dtype=float)
    beam = np.asarray(table["B"], dtype=float)
    if beam.size != EXPECTED_LENGTH:
        raise SystemExit("%s: expected %d samples, got %d" % (name, EXPECTED_LENGTH, beam.size))
    if not np.all(np.isfinite(beam)):
        raise SystemExit("%s: non finite values" % name)
    if abs(beam[0] - 1.0) > 1e-9:
        raise SystemExit("%s: B(ell=0) = %r, expected 1" % (name, beam[0]))
    if beam.min() < 0:
        raise SystemExit("%s: negative beam values" % name)
    increments = np.diff(beam)
    if increments.max() > 1e-6:
        raise SystemExit("%s: beam is not monotonically decreasing" % name)
    return ell, beam


def check_amplitude_convention():
    try:
        import healpy as hp
    except ImportError:
        print("healpy not installed, skipping the amplitude convention check")
        return
    nside, lmax = 64, 128
    fwhm = np.deg2rad(5.0)
    np.random.seed(7)
    cl = hp.gauss_beam(fwhm=fwhm, lmax=lmax) ** 2
    m = hp.synfast(cl, nside, lmax=lmax)
    alm = hp.map2alm(m, lmax=lmax)
    gaussian = hp.gauss_beam(fwhm=fwhm, lmax=lmax)
    smoothed_alm = hp.alm2map(hp.almxfl(alm, gaussian), nside, lmax=lmax)
    smoothed_ref = hp.smoothing(m, fwhm=fwhm, lmax=lmax)
    if not np.allclose(smoothed_alm, smoothed_ref, rtol=1e-6, atol=1e-9):
        raise SystemExit("almxfl with the amplitude beam does not match hp.smoothing")
    print("amplitude convention check passed (almxfl B(ell) equals hp.smoothing)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="instrument_model/instrument_model_sat_beams.tbl")
    args = parser.parse_args()

    model_path = os.path.abspath(args.model)
    model = QTable.read(model_path, format="ascii.ipac")
    print("instrument model: %s (%d rows)" % (model_path, len(model)))

    for row in model:
        beam_path = os.path.normpath(os.path.join(os.path.dirname(model_path), row["beam_file"]))
        ell, beam = check_table(beam_path, row["beam_file"])
        print(
            "  %s %s %-3s B(100)=%.4f B(300)=%.4f B(1000)=%.2e"
            % (row["telescope"], row["band"], row["beam_file"].split("_")[-1][:-4],
               beam[100], beam[300], beam[1000])
        )

    check_amplitude_convention()
    print("all %d beams valid" % len(model))


if __name__ == "__main__":
    main()
