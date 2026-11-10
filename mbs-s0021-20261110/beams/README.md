# Beam tables

28 IPAC tables, `beam_{telescope}_{band}_{ws}.tbl`, one per telescope, band and
focal plane wafer slot, produced by `convert_beams_to_mbs.py` from the Simons
Observatory `20261104_bessel` per-wafer npz product.

Each table has two columns, `ell` (0 to 1999) and `B(ell)`, the amplitude beam
window function normalized to 1 at ell = 0, ready for the mapsims `beam_file`
column (mapsims reads the `B` column and PySM multiplies it into the alms).

## Source

`/scratch/gpfs/SIMONSOBS/sat-iso/beams/planets/20261104_bessel/20261104_bessel_ISO_beam_fitting_results_{telescope}_{ws}_{band}.npz`,
28 files of about 128 MB. Relevant keys:

- `TF_corrected_B_l`: beam transform coefficient, ell 0 to 1999
- `TF_corrected_B_theta`, `theta_arcmin`: radial profile
- `TF_corrected_omega_b`: TF corrected solid angle
- `TF_corrected_fwhm`: TF corrected FWHM in arcmin
- `lmax`: largest multipole of the Bessel fit
- `TF_B_l_cov`, `cov_Bl_analytic`, `cov_Bl_lmax`, `cov_Bl_theta1`: covariances

The product was written with numpy 2; load it with a numpy 2 environment.

## Conversion

```
B(ell) = |TF_corrected_B_l| * (2 pi / TF_corrected_omega_b)
```

then divide by `B(0)`. For `ell > lmax` the stored values are a fit artifact, so
the tail is replaced by a Gaussian with the measured FWHM, matched at `lmax`:

```
B(ell) = B(lmax) * exp(-0.5 * (ell (ell + 1) - lmax (lmax + 1)) sigma^2)
```

with `sigma = FWHM / (60 * 2.355)` in radians.

## Plots

```bash
python plot_beams.py
python plot_beams_diagnostic.py --raw beams_raw.npz
```

`plot_beams.py` makes `beams_all.png` from the tables alone. The diagnostic plot
also needs `beams_raw.npz`, a dump of the raw `TF_corrected_B_l` per channel, not
committed because it is 1.5 MB of duplicated numbers. `convert_beams_to_mbs.py
--dump-arrays` writes the adopted arrays, and the raw dump is a two line numpy
save on Tiger3.

## Validation

```bash
python validate_beams.py
```

Reads the instrument model and every beam table with astropy, the exact call
mapsims makes, and checks normalization, monotonicity and the amplitude
convention against `hp.smoothing`.
