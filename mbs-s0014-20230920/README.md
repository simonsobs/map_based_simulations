# Map-based noise simulations based on the SAT `mbs-noise-sims-sat` time-domain simulations

Tag: `mbs-s0014-20230920`

## Updates

* 2023-09-20: first release.

## Summary

300 realistic realizations of the SAT map noise, estimated from the [mbs-noise-sims-sat](https://github.com/simonsobs/pwg-scripts/tree/master/pwg-tds/mbs-noise-sims-sat) time-domain noise simulations. Simulations cover the full SAT footprint and utilize the tiled noise model.

## Noise model

This release is based on the [mbs-noise-sims-sat](https://github.com/simonsobs/pwg-scripts/tree/master/pwg-tds/mbs-noise-sims-sat) time-domain simulations, available on `NERSC` at:

    /global/cfs/cdirs/sobs/sims/sat-noise-sims/v1

These time-domain simulations include detector and atmospheric noise scaled to match a full year of sensitivity split into two disjoint maps for each frequency band. 

Using [`mnms`](https://github.com/simonsobs/mnms), we generate 300 realizations of the noise using map-based methods. Specifically, we use the tiled model, governed by the configured [parameters](parameters/so_sat_v1_f1.yaml).

Notes:
* Both time-domain and map-domain simulations are stored in HEALPix format. See [examples](#example-usage) below for further guidance.
* A mask has been applied to the map-domain simulations. The masks are stored here: `/global/cfs/cdirs/sobs/v4_sims/mbs/mbs_s0014_20230920/car/masks/coadd_SAT_{bands}_mask_obs_hp.fits`.
* See these [slides](https://drive.google.com/file/d/1ZkwpjYQVCkmbRk5RWOp0Qq4CPsynBH31/view?usp=sharing) for validation of the map-based simulations.

## Available maps

Maps are available in the HEALPix format. Maps are in Equatorial Coordinates, `K_CMB` units, FITS format.

The maps are available on `NERSC` at:

    /global/cfs/cdirs/sobs/v4_sims/mbs/mbs_s0014_20230920/out/run00

and have the following naming convention:

```python
so_sat_v1_f1_tile_{band}_2way_set{split_num}_noise_sim_map{sim_num:04}.fits
```

where `band` is in `[f030, f040, f090, f150, f230, f290]`, `split_num` is in `[0-1]` and `sim_num` is in `[0000-0299]`. Note that the `split_num` is 0-indexed for the map-based sims, while it is 1-indexed for the TOD sims.

Please [open an issue here](https://github.com/simonsobs/map_based_simulations/issues/new) for any data access problems.

## Example usage

```python
import os
import numpy as np
import healpy as hp

opj = os.path.join

# First get some basic info like the path and the filename template.
fdir = '/global/cfs/cdirs/sobs/v4_sims/mbs/mbs_s0014_20230920/out/run00'
fbase_template = 'so_sat_v1_f1_tile_{band}_2way_set{split_num}_noise_sim_map{sim_num:04}.fits'

# Let's load the sim for e.g. f150, split 0, sim 123.
band = 'f150'
split_num = 0
sim_num = 123               # Has 4 digits (leading 0's), but padding done for us in template.

sim = hp.read_map(
    opj(fdir, fbase_template.format(
        band=band,
        split_num=split_num,
        sim_num=sim_num)
        ),
    field=None  # Load I, Q, and U maps in one go. First axis denotes Stokes I, Q and U.
    )
print(sim.shape, sim.dtype)
```
This should give:
```python
(3, 3145728), float32 
```

## Drawing additional simulations

The `runs/run00` script serves as an example of how to draw additional simulations. Note that the script was set up for use on the Simons Foundation cluster. For use on `NERSC`, the script has to be updated with the appropriate filepaths.

The covariance matrices from which simulations are drawn are available here: 

    /global/cfs/cdirs/sobs/v4_sims/mbs/mbs_s0014_20230920/models
    
The masks are stored here:

    /global/cfs/cdirs/sobs/v4_sims/mbs/mbs_s0014_20230920/car/masks


## Preprocessing the TOD simulations

To derive the models, the TOD sims have been preprocessed. This process consists of calling the `project2car.py`, `compare_spectra.py`, `inpaint.py` and `get_masks.py` scripts in order. This is not necessary to repeat, but scripts are included for completeness.

## Feedback

If anything looks suspicious in the simulations, please do not hesitate to [open an issue here](https://github.com/simonsobs/mnms/issues/new).
