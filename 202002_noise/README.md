Realistic noise version 3.1.1 with MSS1 hitmaps
===============================================

Tag: `mbs-s0008-20200207`

Release date 7 Feb 2020

New noise release using version 3.1.1 of the noise curves from [`so_noise_models`](https://github.com/simonsobs/so_noise_models).

Compared to previous releases:

* Updated noise spectra which include a fix for the atmosphere parameters
* Includes cross-correlations between the 2 bands in the same dichroic tube
* Uses new hitmaps from the MSS1 time domain simulations
* Supports noise splits
* Variable Nside based on channels
* Released in HEALPix and CAR

## Input components

All maps are in `uK_CMB`, IQU, single precision (`float32`)

* For the exact configuration of the noise simulations refer to the `noise.toml` configuration file available in this repository.
For all available options refer to the [`SONoiseSimulator` class in `mapsims`](https://mapsims.readthedocs.io/en/latest/api/mapsims.SONoiseSimulator.html#mapsims.SONoiseSimulator).

## Available maps

Only 1 realizations of the full mission and 1 realization of 4 splits are made available as maps.

Reference frame for noise maps is **Equatorial**.

**Location at NERSC**:

    /project/projectdirs/sobs/v4_sims/mbs/201906_noise_no_lowell

The naming convention is:

    {output_nside}/{content}/{num:04d}/simonsobs_{content}_uKCMB_{telescope}{band:03d}_nside{nside}_{num:04d}.fits"

where:

* `content` is in `[noise]`
* `num` is `0`-`9` for high resolution simulations and `10`-`109` for low resolution simulations.
* `telescope` is `sa` or `la`
* `band` is the channel frequency in GHz

Total disk space used is 1.1 T for the 4096 simulations and 43 GB for the 512 simulations.

Backed up to tape in `~zonca/sobs/mbs/201906_noise_no_lowell`.

## Hitmaps

Relative hitmaps for LAT and SAT are available in the `hitmaps` subfolder of the release. They are normalized to a maximum of 1.
Hitmaps are provided both for `classical` and `opportunistic` scanning strategies, simulations use only the `classical` scanning strategy.
Hitmaps were created using the `create_hitmaps.py` script.

## Software

* The PySM components are available in the [`so_pysm_models`](https://github.com/simonsobs/so_pysm_models) package, version 1.0.0, see the [documentation](https://so-pysm-models.readthedocs.io/en/1.0.dev)
* The noise component and the runner script are available in the [`mapsims`](https://github.com/simonsobs/mapsims) package, version 1.0.0, see the [documentation](https://mapsims.readthedocs.io/en/1.0.dev)
