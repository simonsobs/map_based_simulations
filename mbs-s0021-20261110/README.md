# Map based simulation 21: mbs-0021 (temporary)

Release tag: `mbs-s0021-20261110`.

Status: the release directory is being assembled. This README is a temporary
placeholder, it will be replaced by the full release documentation when the
beams and the instrument model are in place, in
[`simonsobs/map_based_simulations#76 "mbs-0021: SAT per-wafer beams from 20261104_bessel"`](https://github.com/simonsobs/map_based_simulations/pull/76).

## What is here

* [`instrument_model/band_optics_wafer_coupling.md`](instrument_model/band_optics_wafer_coupling.md)
  and the companion CSV: the UFM module of every optics tube and wafer slot,
  per hardware configuration, read from the wiki page "Instrument Diagrams for
  Data Reduction". It is used to document which module each per wafer map is,
  and to join the measured per wafer passbands, which are keyed by module name,
  to the simulation channels, which are keyed by band and wafer slot.

## Scope

The release content is defined by the open issues listed below, which are the
source of truth. In short: per wafer measured SAT beams for f090 and f150, per
wafer measured LAT passbands, simulated per wafer LF bandpasses, and the MBS-16
sky model sets updated for the extragalactic and CMB components.

## Tracking

* `simonsobs/map_based_simulations#74` "[mbs-0021] SAT beams"
* `simonsobs/map_based_simulations#75` "[mbs-0021] SO passbands"
* `simonsobs/map_based_simulations#77` "[mbs-0021] LAT beams"
* `simonsobs/map_based_simulations#78` "[mbs-0021] preparation: instrument model and sky model"
* `simonsobs/map_based_simulations#79` "[mbs-0021] band to optics and wafer coupling"

The release is the SO project milestone DM.06.01.Y4.08, "Running new Simons
Observatory MBS 21 map-based simulation", due 2027-01-31.
