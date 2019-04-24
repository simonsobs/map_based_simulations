High resolution foregrounds with spectral index not varying spatially
=====================================================================

Maps are in **Galactic** reference frame

Release date 25 March 2019

The last version of this file is [available on Github](https://github.com/simonsobs/map_based_simulations/tree/master/201903_highres_foregrounds).
The same folder contains all the configuration files used and the scripts to create SLURM jobs.

## Input components

Each component is saved separately, all maps are in `uK_CMB`, IQU, single precision (`float32`)

Dust, synchrotron, free-free and anomalous microwave emission using the "0" models, i.e. `SO_d0`, `SO_s0`, `SO_f0`, and `SO_a0`, see more details in [in the documentation](https://so-pysm-models.readthedocs.io/en/0.2.dev/highres_templates.html#details-about-individual-models).

These maps are full-sky, you can get the noise maps from [the `201901_gaussian_fg_lensed_cmb_realistic_noise` simulations](https://github.com/simonsobs/map_based_simulations/tree/master/201901_gaussian_fg_lensed_cmb_realistic_noise) to add noise and apply the cut from the scanning strategy.
Another option, if you are interested only in the sky cut, is to use the [`SONoiseSimulator` class from `mapsims`](https://mapsims.readthedocs.io/en/latest/api/mapsims.SONoiseSimulator.html#mapsims.SONoiseSimulator), select `nside` and `scanning_strategy` and access the `hitmap` attribute.

## Available maps

HEALPix maps at high resolution (nside 4096) and low resolution (nside 512), these models are deterministic, so we have
a set for each resolution for all channels.

**Location at NERSC**:

    /project/projectdirs/sobs/v4_sims/mbs/201903_highres_foregrounds

The naming convention is:

    {output_nside}/{content}/{num:04d}/simonsobs_{content}_uKCMB_{telescope}{band:03d}_nside{nside}_{num:04d}.fits"

where:

* `content` is in `[cmb, synchtrotron, freefree, ame]`
* `num` is `0`
* `telescope` is `sa` or `la`
* `band` is the channel frequency in GHz

Backed up to tape in `~zonca/sobs/mbs/201903_highres_foregrounds`.

## Issues or feedback

In case of any problem with the maps or the documentation or request more/different runs, [open an issue on the `map_based_simulations` repo](https://github.com/simonsobs/map_based_simulations/issues)

## Plots

See the `plot_maps.ipynb` notebook in the folder, executed notebooks:

* [Temperature NSIDE 512](https://gist.github.com/240377264d49c2122c9521e0256b0388)
* [Temperature NSIDE 4096](https://gist.github.com/zonca/ce3e58f964ff63ddcc4ef8ac8db74205)
* [Polarization NSIDE 512](https://gist.github.com/25f3947f9d44d88b82e15127441f7bfb)
* [Polarization NSIDE 4096](https://gist.github.com/zonca/35f5d2ed6ff27e8d2f788258218da47c)

## Software

* The PySM components are available in the [`so_pysm_models`](https://github.com/simonsobs/so_pysm_models) package, version 0.2.0, see the [documentation](https://so-pysm-models.readthedocs.io/en/0.2.dev)
* The noise component and the runner script are available in the [`mapsims`](https://github.com/simonsobs/mapsims) package, version 0.2.0, see the [documentation](https://mapsims.readthedocs.io/en/0.2.dev)
