CMB realizations lensed with gaussian potential
===============================================

Tag: `mbs-s0009-20191107`

Released on 7 November 2019 by @zonca

**100** CMB realizations for all channels from [`alms`](https://mapsims.readthedocs.io/en/latest/models.html#available-cosmic-microwave-background-simulations) with best-fit Planck cosmology and gaussian lensing potential.

## Input components

All maps are in `uK_CMB`, IQU, single precision (`float32`)

## Instrument properties

Beams are read from `sotodlib`.

## Available maps

HEALPix maps at high resolution (nside 4096) and low resolution (nside 512), so we have
a set for each resolution for all channels. All maps are full-sky, see [the `201906_noise_no_lowell`  release for hitmaps](https://github.com/simonsobs/map_based_simulations/tree/master/201906_noise_no_lowell).

The `ell_max` for the harmonics transform is `3*Nside-1`.

**Location at NERSC**:

    /project/projectdirs/sobs/v4_sims/mbs/201911_lensed_cmb

The naming convention is:

    {nside}/{content}/{num:04d}/simonsobs_{content}_uKCMB_{telescope}{band}_nside{nside}_{num:04d}.fits"

where:

* `content` is `cmb`
* `num` is from `0` to `99`
* `telescope` is `sa` or `la`
* `band` is the channel band, the options are: `LF1,LF2,MFF1,MFF2,MFS1,MFS2,UHF1,UHF2`

Backed up to tape in `~zonca/sobs/mbs/201911_lensed_cmb`.

## Issues or feedback

In case of any problem with the maps or the documentation or request more/different runs, [open an issue on the `map_based_simulations` repo](https://github.com/simonsobs/map_based_simulations/issues)

## Software

* PySM 3 is available at <https://github.com/healpy/pysm>, version 3.0
* [`sotodlib`](https://github.com/simonsobs/sotodlib) version `7290c1b`
* The PySM components are available in the [`so_pysm_models`](https://github.com/simonsobs/so_pysm_models) package, version 2.1.0, see the [documentation](https://so-pysm-models.readthedocs.io/en/2.3.dev)
* The runner script is available in the [`mapsims`](https://github.com/simonsobs/mapsims) package, version 2.1.0, see the [documentation](https://mapsims.readthedocs.io/en/2.3.dev)
