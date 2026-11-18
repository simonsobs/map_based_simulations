# Band, optics tube and wafer coupling

Reference table that assigns each optics tube and wafer slot of the Simons
Observatory to its UFM module, per hardware configuration, so that a simulated
channel can be connected to the measured product for the same physical array.

Status: prepared for mbs-0021, tracked in
[`simonsobs/map_based_simulations#79 "[mbs-0021] band to optics and wafer coupling"`](https://github.com/simonsobs/map_based_simulations/issues/79).
The SAT assignments and the ASO LAT assignment are complete. The SO nominal LAT
assignment is only partial, see [Open items](#open-items). The document lives in
the release directory of mbs-0021, `mbs-s0021-20261110/instrument_model/`.

## What the table is for

1. **Documenting the per wafer maps of a release.** The mbs-0021 instrument
   model has one SAT channel per telescope, band and wafer slot (satp1 and
   satp3, f090 and f150, ws0 to ws6), see
   [`simonsobs/map_based_simulations#76 "mbs-0021: SAT per-wafer beams from 20261104_bessel"`](https://github.com/simonsobs/map_based_simulations/pull/76).
   The beam product is keyed by `ws` slot, so the slot is already the join key
   between a channel and its beam. What the release cannot say from that key
   alone is which physical module the map represents, and that is what this
   table adds.
2. **Joining the measured LAT passbands.** The 2026 LAT passband release has 28
   per wafer curves, 14 measured wafers times 2 sub-bands, keyed by module name
   (`mv13`, `uv31`, ...). A LAT channel is instead identified by band and wafer
   index, so the module to tube and slot correspondence is needed before a
   measured curve can be attached to the channel it belongs to.
3. **Reference for future releases and for comparisons with real data.**

The table is not needed for the parts of the model that stay band level: the
SAT passbands are four band averaged curves with no wafer decomposition, and
the LAT beams are Gaussian with nominal FWHM, both for mbs-0021.

## Naming conventions

Module names carry the array type in the prefix:

| prefix | array type | bands in mbs | bands in the measured products |
| --- | --- | --- | --- |
| `mv` | MF | `f090`, `f150` | `f090`, `f150` |
| `uv` | UHF, also called HF in some documents | `f230`, `f290` | `f220`, `f280` |
| `lv` | LF | `f030`, `f040` | no per wafer product |

The band names differ between the simulation model and the measured products
for the high frequency arrays: mbs uses `f230` and `f290`, the passband and beam
products use `f220` and `f280`. The table keeps both in the `bands_mbs` and
`bands_product` columns.

## Slot conventions

* LAT: each optics tube has three wafer slots, `ws0`, `ws1`, `ws2`.
* SAT: each telescope has one optics tube with seven wafer slots, `ws0` to
  `ws6`.
* In the mbs-0021 SAT beam table the wafer index of the channel is the `ws`
  slot, so channel, beam and this table share one identifier. In the older
  `mbs-s0016` model the wafer index was a Bandpass Sampler enumeration, with
  eight curves for a band where the hardware has seven slots, and it did not
  follow the hardware.

## The table

The machine readable version is
[`band_optics_wafer_coupling.csv`](band_optics_wafer_coupling.csv), one row per
wafer slot, with columns:

| column | meaning |
| --- | --- |
| `telescope` | `SAT1`, `SAT2`, `SAT3` or `LAT` |
| `configuration` | hardware configuration, see the tables below |
| `optics_tube` | LAT tube name, empty for a SAT |
| `wafer_slot` | `ws0` to `ws6` |
| `module` | UFM module name |
| `module_type` | `MF`, `UHF` or `LF` |
| `bands_mbs` | mbs band names for that module |
| `bands_product` | band names used by the measured products |
| `coverage` | `full` when the whole configuration was transcribed, `partial` otherwise |
| `source_image` | image on the wiki page the row was read from |
| `notes` | footnotes, see [Provenance](#provenance) |

### SATP1

SCR4, up to December 2024 (`sat1_scr4`, image `image-20231108-165754.png`,
titled "SAT-MF1 On Sky"):

| tube | slot | module | type | mbs bands |
| --- | --- | --- | --- | --- |
| - | ws0 | mv19 | MF | f090;f150 |
| - | ws1 | mv18 | MF | f090;f150 |
| - | ws2 | mv22 | MF | f090;f150 |
| - | ws3 | mv29 | MF | f090;f150 |
| - | ws4 | mv7 | MF | f090;f150 |
| - | ws5 | mv9 | MF | f090;f150 |
| - | ws6 | mv15 | MF | f090;f150 |

SCR5, current (`sat1_scr5`, image `image-20250115-191650.png`), the
configuration of the mbs-0021 beams:

| tube | slot | module | type | mbs bands |
| --- | --- | --- | --- | --- |
| - | ws0 | mv19 | MF | f090;f150 |
| - | ws1 | mv48 | MF | f090;f150 |
| - | ws2 | mv50 | MF | f090;f150 |
| - | ws3 | mv22 | MF | f090;f150 |
| - | ws4 | mv18 | MF | f090;f150 |
| - | ws5 | mv52 | MF | f090;f150 |
| - | ws6 | mv51 | MF | f090;f150 |

### SATP2

Run 6, up to March 2025 (`sat2_run6`, image `sat-uhf-fpa.png`, titled "SATP2 On
Sky"):

| tube | slot | module | type | mbs bands |
| --- | --- | --- | --- | --- |
| - | ws0 | uv41 | UHF | f230;f290 |
| - | ws1 | uv8 | UHF | f230;f290 |
| - | ws2 | uv37 | UHF | f230;f290 |
| - | ws3 | uv45 | UHF | f230;f290 |
| - | ws4 | uv36 | UHF | f230;f290 |
| - | ws5 | uv44 | UHF | f230;f290 |
| - | ws6 | uv40 | UHF | f230;f290 |

Run 7, current (`sat2_run7`, image `image-20251103-151602.png`, titled "SATP2
Nominal (On Sky)"):

| tube | slot | module | type | mbs bands |
| --- | --- | --- | --- | --- |
| - | ws0 | uv41 | UHF | f230;f290 |
| - | ws1 | uv45 | UHF | f230;f290 |
| - | ws2 | uv53 | UHF | f230;f290 |
| - | ws3 | uv40 | UHF | f230;f290 |
| - | ws4 | uv8 | UHF | f230;f290 |
| - | ws5 | uv37 | UHF | f230;f290 |
| - | ws6 | uv56 | UHF | f230;f290 |

The SATP2 assignment changed between Run 6 and Run 7: `ws3`, `ws5` and `ws6`
carry different modules in the two runs.

### SATP3

ST3 nominal (`sat3`, image `image-20231201-164023.png`):

| tube | slot | module | type | mbs bands |
| --- | --- | --- | --- | --- |
| - | ws0 | mv5 | MF | f090;f150 |
| - | ws1 | mv27 | MF | f090;f150 |
| - | ws2 | mv35 | MF | f090;f150 |
| - | ws3 | mv12 | MF | f090;f150 |
| - | ws4 | mv23 | MF | f090;f150 |
| - | ws5 | mv33 | MF | f090;f150 |
| - | ws6 | mv17 | MF | f090;f150 |

All three deployed SATs are either MF (SATP1, SATP3) or UHF (SATP2). No SAT LF
array is shown on the page.

### LAT, ASO configuration as of early 2026

(`lat_aso_2026`, images `image-20260427-162101.png` and
`image-20260427-163328.png`, titled "ASO LAT"):

| tube | slot | module | type | mbs bands |
| --- | --- | --- | --- | --- |
| c1 | ws0 | uv38 | UHF | f230;f290 |
| c1 | ws1 | uv39 | UHF | f230;f290 |
| c1 | ws2 | uv46 | UHF | f230;f290 |
| i1 | ws0 | mv21 | MF | f090;f150 |
| i1 | ws1 | mv24 | MF | f090;f150 |
| i1 | ws2 | mv28 | MF | f090;f150 |
| i2 | ws0 | uv54 | UHF | f230;f290 |
| i2 | ws1 | uv60 | UHF | f230;f290 |
| i2 | ws2 | uv58 | UHF | f230;f290 |
| i3 | ws0 | mv13 | MF | f090;f150 |
| i3 | ws1 | mv20 | MF | f090;f150 |
| i3 | ws2 | mv34 | MF | f090;f150 |
| i4 | ws0 | mv14 | MF | f090;f150 |
| i4 | ws1 | mv32 | MF | f090;f150 |
| i4 | ws2 | mv49 | MF | f090;f150 |
| i5 | ws0 | uv31 | UHF | f230;f290 |
| i5 | ws1 | uv42 | UHF | f230;f290 |
| i5 | ws2 | uv47 | UHF | f230;f290 |
| i6 | ws0 | mv25 | MF | f090;f150 |
| i6 | ws1 | mv26 | MF | f090;f150 |
| i6 | ws2 | mv11 | MF | f090;f150 |
| o1 | ws0 | uv57 | UHF | f230;f290 |
| o1 | ws1 | uv59 | UHF | f230;f290 |
| o1 | ws2 | uv62 | UHF | f230;f290 |
| o2 | ws0 | mv29 | MF | f090;f150 |
| o2 | ws1 | mv68 | MF | f090;f150 |
| o2 | ws2 | mv73 | MF | f090;f150 |
| o3 | ws0 | mv65 | MF | f090;f150 |
| o3 | ws1 | mv67 | MF | f090;f150 |
| o3 | ws2 | mv75 | MF | f090;f150 |
| o4 | ws0 | mv15 [1] | MF | f090;f150 |
| o4 | ws1 | mv64 | MF | f090;f150 |
| o4 | ws2 | mv70 | MF | f090;f150 |
| o5 | ws0 | mv77 | MF | f090;f150 |
| o5 | ws1 | mv63 | MF | f090;f150 |
| o5 | ws2 | mv76 | MF | f090;f150 |
| o6 | ws2 | lv11 | LF | f030;f040 |

The LF tube o6 shows a single large wafer at `ws2` in this diagram, with no
wafer at `ws0` and `ws1`.

### LAT, SO nominal configuration

(`lat_nominal_2025`, partial, image `image-20231201-025152.png`, titled "LAT i1
Nominal"):

| tube | slot | module | type | mbs bands |
| --- | --- | --- | --- | --- |
| i1 | ws0 | mv21 [2] | MF | f090;f150 |
| i1 | ws1 | mv24 [2] | MF | f090;f150 |
| i1 | ws2 | mv28 [2] | MF | f090;f150 |

## Provenance

All rows were read from the diagrams on the wiki page
[Instrument Diagrams for Data Reduction](https://simonsobs.atlassian.net/wiki/spaces/DM/pages/210894849)
(DM space, page 210894849), which shows the UFMs and their wafer slots as
projected on sky, per telescope and per observing run. The `source_image`
column names the attachment the row comes from, so every entry can be checked
against the figure.

The diagrams are raster images and the values are not available in machine
readable form anywhere else, so the labels were transcribed by eye from the
attached PNG files. Anything used to attach a measured product to a simulation
channel should first be confirmed with the instrument model team.

Notes:

* **[1]** The `o4` `ws0` label is rendered as `mv15r2` in the diagram and the
  last characters are ambiguous. The module number needs confirmation before
  the row is used.
* **[2]** The SO nominal LAT configuration has no fully labelled diagram on the
  page, only a zoom of the `i1` tube and a two tube schematic. The three `i1`
  values are the ones that can be read; the other tubes are missing from the
  table and the `coverage` column marks the configuration as `partial`.

## Reconciliation with the measured products

**SAT.** The mbs-0021 model has 14 `f090` and 14 `f150` channels, satp1 and
satp3 times `ws0` to `ws6`, with beams from `20261104_bessel`, which is strictly
the SCR5 configuration for satp1. The `sat1_scr5` and `sat3` rows of this table
therefore describe the hardware behind those channels. SATP2 is UHF and its
beams stay Gaussian, so its module assignment is documentation only.

**LAT.** The 2026 LAT passband release has 28 curves from 8 MF and 6 UHF wafers:

* the 6 UHF modules, `uv31`, `uv38`, `uv39`, `uv42`, `uv46`, `uv47`, are the
  three slots of `c1` and the three slots of `i5`, that is all six UHF slots of
  the nominal LAT;
* the 8 MF modules, `mv13`, `mv14`, `mv20`, `mv24`, `mv28`, `mv32`, `mv34`,
  `mv49`, are all of `i3` and `i4` plus `i1` `ws1` and `i1` `ws2`. The
  remaining MF slots are the three of `i6` and `i1` `ws0` (`mv21`), which
  accounts for a coverage of 8 out of the 12 MF slots.

**LF.** There is no measured per wafer LF product. The `f030` and `f040`
channels, four wafers each for SAT and LAT, are simulated with the Bandpass
Sampler tables already used in `mbs-s0016`, so they need no module join.

## How to use the table

1. Pick the configuration that the simulation represents and record it in the
   release README. For SAT the assignment depends on the observing run, so name
   the run, not only the telescope.
2. SAT channels: the channel already carries the `ws` slot, which is the beam
   key. Read the module for that slot here to document the map.
3. LAT channels: look up the module of a measured passband curve here to obtain
   its optics tube and slot, then map that to the channel naming chosen by the
   release.
4. Band naming differences between the products and mbs (`f220`, `f280` against
   `f230`, `f290`) are documented in `bands_product`.

## Verification

The CSV can be checked with:

```python
import csv
from collections import Counter

rows = list(csv.DictReader(open("band_optics_wafer_coupling.csv")))

keys = [(r["configuration"], r["telescope"], r["optics_tube"], r["wafer_slot"]) for r in rows]
assert len(keys) == len(set(keys)), "duplicated slot"

prefix_types = {"m": "MF", "u": "UHF", "l": "LF"}
for r in rows:
    assert prefix_types[r["module"][0]] == r["module_type"], r

print(Counter((r["configuration"], r["coverage"]) for r in rows))
```

## Open items

* Confirm the ambiguous `o4` `ws0` module and the `o6` LF slot occupancy with
  the instrument model team.
* Complete the SO nominal LAT assignment, which is not fully labelled on the
  diagrams.
* Decide the LAT channel naming for the measured per wafer passbands, and name
  the tube and slot, or the module, in the release instrument model.
* Decide whether the LAT assignment should follow the ASO configuration of
  early 2026, the configuration the measurements come from, or the SO nominal
  one used by `mbs-s0016`.
