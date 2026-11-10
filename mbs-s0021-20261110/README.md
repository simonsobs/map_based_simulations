# mbs-0021 SAT beams

Per-wafer SAT beam window functions for the next map based simulations release,
converted from the Simons Observatory product `20261104_bessel` (the strictly
SCR5 product recommended in the Beams Metadata Version Log since 2026-11-05).

This directory contains the SAT f090 and f150 beams only. The other SAT bands
stay Gaussian at the nominal instrument model FWHM, which is identical to the
one in mbs-s0016 because no measured SAT LF or UHF beam product exists yet:

| Band | FWHM (arcmin) | Status |
|---|---|---|
| f030 | 91.0 | nominal, not measured |
| f040 | 63.0 | nominal, not measured |
| f090 | 27.6 to 28.4 | measured, 20261104_bessel |
| f150 | 19.4 to 19.8 | measured, 20261104_bessel |
| f230 | 11.0 | nominal, not measured |
| f290 | 9.0 | nominal, not measured |

The nominal values come from `sotodlib.sim_hardware.sim_nominal()` and are
unchanged from `mbs-s0016-20241111`. They are placeholders: for the two MF bands
the measurements differ from the nominal 30.0 and 17.0 by about 1 to 3 arcmin.

## Contents

- `beams/beam_{telescope}_{band}_{ws}.tbl`: 28 IPAC tables, one per telescope
  (satp1, satp3), band (f090, f150) and focal plane wafer slot (ws0 to ws6),
  columns `ell` and `B(ell)`.
- `beams/beam_summary.csv`: FWHM, solid angle, fit lmax and a few B(ell) values
  per channel.
- `beams/beams_all.png`: all 28 beams with a Gaussian reference per panel.
- `beams/beams_raw_vs_adopted.png`: raw product against the adopted beam for
  three representative channels, showing why the high ell tail is replaced.
- `beams/convert_beams_to_mbs.py`: converts the product npz to the tables.
- `beams/plot_beams.py`, `beams/plot_beams_diagnostic.py`: make the plots.
- `beams/validate_beams.py`: checks the tables the way mapsims reads them.
- `instrument_model/instrument_model_sat_beams.tbl`: one row per beam, with the
  `beam_file` column mapsims uses for custom beams.
- `make_instrument_model.py`: builds the instrument model from the summary.
- `common.toml`: example configuration pointing at the SAT beam model.

## Regenerating

The conversion reads the per-wafer npz directly from Tiger3, which needs numpy 2
(the files were written with numpy 2 and fail to load pickled arrays with the
system numpy 1.23):

```bash
module load soconda/3.12/v0.6.16
python beams/convert_beams_to_mbs.py \
  --input-dir /scratch/gpfs/SIMONSOBS/sat-iso/beams/planets/20261104_bessel \
  --output-dir beams
python make_instrument_model.py
python beams/validate_beams.py
```

`make_instrument_model.py` writes the table with plain Python, no astropy needed.
`convert_beams_to_mbs.py` needs numpy only. `validate_beams.py` needs astropy and
optionally healpy.

## Beam convention

mapsims passes the custom beam to PySM as `beam_window`, which multiplies the
alms, so the tables hold the **amplitude** beam

```
B(ell) = |TF_corrected_B_l| * (2 pi / TF_corrected_omega_b)
```

renormalized to 1 at ell = 0. The product itself is about 0.3 percent above 1 at
ell = 0 (0.3 to 1.0 percent per channel), and it stores `B_l` with a global minus
sign from the transform convention.

## Two caveats of the product

1. **The Bessel fit is only valid up to `lmax`** (744 to 859 for f090, 1170 to
   1223 for f150). Beyond `lmax` the stored `B(ell)` oscillates and floors at
   about 1e-3 instead of decaying, which would put spurious power at high ell.
   The conversion replaces everything beyond `lmax` with a Gaussian of the
   measured FWHM, matched in value at `lmax`. See
   `beams/beams_raw_vs_adopted.png` and the discussion in
   `simonsobs/map_based_simulations#74 "[mbs-0021] SAT beams"`.
2. **SAT1 ws3 f090 is the problematic channel**: its TF estimation failed and was
   replaced with the ws5 f090 transfer function, and only Saturn was available
   for the peak fit. The product documentation hopes it has little weight in the
   CMB maps.

`TF_corrected_*` includes the transfer function correction, as recommended by the
product page (the correction adds power back into the beam, solid angle and
window function).

## Using it with mapsims

Every row of a table that has a `beam_file` column must name a beam file, so this
model has only the 28 SAT beam rows. To run the full mbs-0021 model, merge these
rows with the other bands and the LAT (which still use a Gaussian `fwhm` and no
`beam_file`), producing a table where every row has a beam file, or generate
Gaussian tables for the remaining channels.

## Provenance

- Product: `20261104_bessel`, on Tiger3 at
  `/scratch/gpfs/SIMONSOBS/sat-iso/beams/planets/20261104_bessel/`
- Beams Metadata Version Log:
  https://simonsobs.atlassian.net/wiki/spaces/DM/pages/2025291968
- Beam author: Sam Day-Weiss (Princeton), beam point of contact designated by
  Sara Simon.
