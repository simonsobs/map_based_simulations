Extragalactic emission with Websky
==================================

Release date 20 May 2019

The last version of this file is [available on Github](https://github.com/simonsobs/map_based_simulations/tree/master/201905_extragalactic).
The same folder contains all the configuration files used and the scripts to create SLURM jobs.

## Input components

Each component is saved separately, all maps are in `uK_CMB`, I, single precision (`float32`)

The CIB, KSZ and TSZ models are created from WebSky cosmological simulations, 
we also include one CMB realization generated with the same cosmological parameters used in the WebSky simulations both unlensed and lensed with the potential from the WebSky simulations,
see more details in [in the documentation](https://so-pysm-models.readthedocs.io/en/latest/models.html#websky).

These maps are full-sky, you can get the noise maps from [the `201901_gaussian_fg_lensed_cmb_realistic_noise` simulations](https://github.com/simonsobs/map_based_simulations/tree/master/201901_gaussian_fg_lensed_cmb_realistic_noise) to add noise and apply the cut from the scanning strategy.
Another option, if you are interested only in the sky cut, is to use the [`SONoiseSimulator` class from `mapsims`](https://mapsims.readthedocs.io/en/latest/api/mapsims.SONoiseSimulator.html#mapsims.SONoiseSimulator), select `nside` and `scanning_strategy` and access the `hitmap` attribute.

## Available maps

HEALPix maps at high resolution (nside 4096) and low resolution (nside 512), these models are deterministic, so we have
a set for each resolution for all channels.

Reference frame for the maps is **Equatorial**.
Bandpass for each channel is a **delta function** centered at the reference frequency.
Beams as defined in the [`SO_Noise_Calculator`](https://github.com/simonsobs/mapsims/blob/master/mapsims/SO_Noise_Calculator_Public_20180822.py) released in October 2018.
The `ell_max` for the harmonics transform is `3*Nside-1`

**Location at NERSC**:

    /project/projectdirs/sobs/v4_sims/mbs/201905_extragalactic

The naming convention is:

    {output_nside}/{content}/{num:04d}/simonsobs_{content}_uKCMB_{telescope}{band:03d}_nside{nside}_{num:04d}.fits"

where:

* `content` is in `[cib, ksz, tsz, cmb, cmb_unlensed]`
* `num` is `0`
* `telescope` is `sa` or `la`
* `band` is the channel frequency in GHz

Backed up to tape in `~zonca/sobs/mbs/201905_extragalactic`.

## Issues or feedback

In case of any problem with the maps or the documentation or request more/different runs, [open an issue on the `map_based_simulations` repo](https://github.com/simonsobs/map_based_simulations/issues)

## Plots

See the `plot_maps.ipynb` notebook in the folder, executed notebooks:

* [NSIDE 512](https://gist.github.com/71617c6a4c25191fa694375fe95672c6)
* [NSIDE 4096](https://gist.github.com/45f2ca0d26fb2cfd2dd67b38298b2618)

## Software

* The PySM components are available in the [`so_pysm_models`](https://github.com/simonsobs/so_pysm_models) package, version 1.0.0, see the [documentation](https://so-pysm-models.readthedocs.io/en/latest)
* The noise component and the runner script are available in the [`mapsims`](https://github.com/simonsobs/mapsims) package, version 1.0.0, see the [documentation](https://mapsims.readthedocs.io/en/latest)
* [Development version of PySM 3](https://github.com/healpy/pysm)
* [Development version of healpy](https://github.com/healpy/healpy), for smoothing alms in place, it will be available in healpy `1.3.0`

## Performance

At 4096 with lmax to `3*nside` **each frequency channel** (e.g. `LA_27`, `SA_27`): 1 minute  single node on Popeye (SDSC), possibly very quick because it is temperature only. At 512 1 minute **all channels**.
