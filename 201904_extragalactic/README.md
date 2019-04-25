High resolution foregrounds with spectral index varying spatially
=====================================================================

Release date 24 April 2019

The last version of this file is [available on Github](https://github.com/simonsobs/map_based_simulations/tree/master/201904_extragalactic).
The same folder contains all the configuration files used and the scripts to create SLURM jobs.

## Input components

Each component is saved separately, all maps are in `uK_CMB`, IQU, single precision (`float32`)

Extragalactic Cosmic Infrared Background, Thermal and Kinetic SZ effects,, see more details in [in the documentation](https://so-pysm-models.readthedocs.io/en/0.3.dev/models.html#websky)

These maps are full-sky, you can get the noise maps from [the `201901_gaussian_fg_lensed_cmb_realistic_noise` simulations](https://github.com/simonsobs/map_based_simulations/tree/master/201901_gaussian_fg_lensed_cmb_realistic_noise) to add noise and apply the cut from the scanning strategy.
Another option, if you are interested only in the sky cut, is to use the [`SONoiseSimulator` class from `mapsims`](https://mapsims.readthedocs.io/en/latest/api/mapsims.SONoiseSimulator.html#mapsims.SONoiseSimulator), select `nside` and `scanning_strategy` and access the `hitmap` attribute.

## Available maps

HEALPix maps at high resolution (nside 4096) and low resolution (nside 512), these models are deterministic, so we have
a set for each resolution for all channels.

Reference frame for the maps is **Equatorial**
Bandpass for each channel is a **delta function** centered at the reference frequency.
Beams as defined in the [`SO_Noise_Calculator`](https://github.com/simonsobs/mapsims/blob/master/mapsims/SO_Noise_Calculator_Public_20180822.py) released in October 2018.

**Location at NERSC**:

    /project/projectdirs/sobs/v4_sims/mbs/201904_extragalactic

The naming convention is:

    {output_nside}/{content}/{num:04d}/simonsobs_{content}_uKCMB_{telescope}{band:03d}_nside{nside}_{num:04d}.fits"

where:

* `content` is in `[cib, ksz, tsz]`
* `num` is `0`
* `telescope` is `sa` or `la`
* `band` is the channel frequency in GHz

Backed up to tape in `~zonca/sobs/mbs/201904_extragalactic`.

## Issues or feedback

In case of any problem with the maps or the documentation or request more/different runs, [open an issue on the `map_based_simulations` repo](https://github.com/simonsobs/map_based_simulations/issues)

## Plots

See the `plot_maps.ipynb` notebook in the folder, executed notebooks:

* [NSIDE 512](https://gist.github.com/zonca/b0fd1fe3f698000c81be57b69636e4a4)
* [NSIDE 4096](https://gist.github.com/0ef102bf777b541c3d669d0d7b22555c)

## Software

* The PySM components are available in the [`so_pysm_models`](https://github.com/simonsobs/so_pysm_models) package, version 0.3.0, see the [documentation](https://so-pysm-models.readthedocs.io/en/0.3.dev)
* The noise component and the runner script are available in the [`mapsims`](https://github.com/simonsobs/mapsims) package, version 0.3.0, see the [documentation](https://mapsims.readthedocs.io/en/0.3.dev)
