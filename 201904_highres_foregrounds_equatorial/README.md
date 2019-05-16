High resolution foregrounds with spectral index not varying spatially
=====================================================================

Release date 24 April 2019

This is a re-run of the [`201903_highres_foregrounds`](https://github.com/simonsobs/map_based_simulations/tree/master/201903_highres_foregrounds) simulations in **Equatorial** coordinates instead of **Galactic**. The only other difference is that `hp.smoothing` now uses `use_pixel_weights=True`, i.e. the spherical harmonics transform should be of slightly better quality.

The last version of this file is [available on Github](https://github.com/simonsobs/map_based_simulations/tree/master/201904_highres_foregrounds_equatorial).
The same folder contains all the configuration files used and the scripts to create SLURM jobs.

## Input components

Each component is saved separately, all maps are in `uK_CMB`, IQU, single precision (`float32`)

Dust, synchrotron, free-free and anomalous microwave emission using the "0" models, i.e. `SO_d0`, `SO_s0`, `SO_f0`, and `SO_a0`, see more details in [in the documentation](https://so-pysm-models.readthedocs.io/en/0.2.dev/highres_templates.html#details-about-individual-models).

These maps are full-sky, you can get the noise maps from [the `201901_gaussian_fg_lensed_cmb_realistic_noise` simulations](https://github.com/simonsobs/map_based_simulations/tree/master/201901_gaussian_fg_lensed_cmb_realistic_noise) to add noise and apply the cut from the scanning strategy.
Another option, if you are interested only in the sky cut, is to use the [`SONoiseSimulator` class from `mapsims`](https://mapsims.readthedocs.io/en/latest/api/mapsims.SONoiseSimulator.html#mapsims.SONoiseSimulator), select `nside` and `scanning_strategy` and access the `hitmap` attribute.

## Available maps

HEALPix maps at high resolution (nside 4096) and low resolution (nside 512), these models are deterministic, so we have
a set for each resolution for all channels.

Reference frame for the maps is **Equatorial**.
Bandpass for each channel is a **delta function** centered at the reference frequency.
Beams as defined in the [`SO_Noise_Calculator`](https://github.com/simonsobs/mapsims/blob/master/mapsims/SO_Noise_Calculator_Public_20180822.py) released in October 2018.

**Location at NERSC**:

    /project/projectdirs/sobs/v4_sims/mbs/201904_highres_foregrounds_equatorial

The naming convention is:

    {output_nside}/{content}/{num:04d}/simonsobs_{content}_uKCMB_{telescope}{band:03d}_nside{nside}_{num:04d}.fits"

where:

* `content` is in `[cmb, synchtrotron, freefree, ame]`
* `num` is `0`
* `telescope` is `sa` or `la`
* `band` is the channel frequency in GHz

Backed up to tape in `~zonca/sobs/mbs/201904_highres_foregrounds_equatorial`.

## Issues or feedback

In case of any problem with the maps or the documentation or request more/different runs, [open an issue on the `map_based_simulations` repo](https://github.com/simonsobs/map_based_simulations/issues)

## Plots

See the `plot_maps.ipynb` notebook in the folder, executed notebooks:

* [NSIDE 512](https://gist.github.com/0e6d1a16f4afdb1dcc7859f3262fdd9f)
* [NSIDE 4096]() not available yet

## Software

* The PySM components are available in the [`so_pysm_models`](https://github.com/simonsobs/so_pysm_models) package, version 0.3.0, see the [documentation](https://so-pysm-models.readthedocs.io/en/0.3.dev)
* The noise component and the runner script are available in the [`mapsims`](https://github.com/simonsobs/mapsims) package, version 0.3.0, see the [documentation](https://mapsims.readthedocs.io/en/0.3.dev)

## Performance

At 4096 with lmax to `2*nside`: 115 minutes for synchrotron and dust, 95 minutes for freefree and ame, single node on Popeye (SDSC)
