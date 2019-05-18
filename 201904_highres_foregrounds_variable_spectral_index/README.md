High resolution foregrounds in Equatorial with spectral index varying spatially
===============================================================================

Release date 17 May 2019

Also, this is the first set of simulations which uses the development version of [PySM 3](https://github.com/healpy/pysm).

The last version of this file is [available on Github](https://github.com/simonsobs/map_based_simulations/tree/master/201904_highres_foregrounds_variable_spectral_index).
The same folder contains all the configuration files used and the scripts to create SLURM jobs.

## Input components

Each component is saved separately, all maps are in `uK_CMB`, IQU or I, single precision (`float32`)

Dust, synchrotron, free-free and anomalous microwave emission using the "1" models, i.e. `SO_d1`, `SO_s1`, and `SO_a1`, see more details in [in the documentation](https://so-pysm-models.readthedocs.io/en/1.0.dev/highres_templates.html#details-about-individual-models).

These maps are full-sky, you can get the noise maps from [the `201901_gaussian_fg_lensed_cmb_realistic_noise` simulations](https://github.com/simonsobs/map_based_simulations/tree/master/201901_gaussian_fg_lensed_cmb_realistic_noise) to add noise and apply the cut from the scanning strategy.
Another option, if you are interested only in the sky cut, is to use the [`SONoiseSimulator` class from `mapsims`](https://mapsims.readthedocs.io/en/latest/api/mapsims.SONoiseSimulator.html#mapsims.SONoiseSimulator), select `nside` and `scanning_strategy` and access the `hitmap` attribute.

## Available maps

HEALPix maps at high resolution (nside 4096) and low resolution (nside 512), these models are deterministic, so we have
a set for each resolution for all channels.

Reference frame for the maps is **Equatorial**.
Bandpass for each channel is a **delta function** centered at the reference frequency.
Beams as defined in the [`SO_Noise_Calculator`](https://github.com/simonsobs/mapsims/blob/master/mapsims/SO_Noise_Calculator_Public_20180822.py) released in October 2018.
The `ell_max` for the harmonics transform is `3*Nside-1`, in the `ellmax_2nside` subfolder the same simulations were executed just up to `2*Nside`.

**Location at NERSC**:

    /project/projectdirs/sobs/v4_sims/mbs/201904_highres_foregrounds_variable_spectral_index

The naming convention is:

    {output_nside}/{content}/{num:04d}/simonsobs_{content}_uKCMB_{telescope}{band:03d}_nside{nside}_{num:04d}.fits"

where:

* `content` is in `[cmb, synchtrotron, ame]`
* `num` is `0`
* `telescope` is `sa` or `la`
* `band` is the channel frequency in GHz

Backed up to tape in `~zonca/sobs/mbs/201904_highres_foregrounds_variable_spectral_index`.

## Issues or feedback

In case of any problem with the maps or the documentation or request more/different runs, [open an issue on the `map_based_simulations` repo](https://github.com/simonsobs/map_based_simulations/issues)

## Plots

See the `plot_maps.ipynb` notebook in the folder, executed notebooks:

* [NSIDE 512](https://gist.github.com/ac0beefc53475e9a9dd6fc3e457907b4)
* [NSIDE 4096](https://gist.github.com/f10061b1059b2318ee91584397eb2f8b)

## Software

* The PySM components are available in the [`so_pysm_models`](https://github.com/simonsobs/so_pysm_models) package, version 1.0.0, see the [documentation](https://so-pysm-models.readthedocs.io/en/1.0.dev)
* The noise component and the runner script are available in the [`mapsims`](https://github.com/simonsobs/mapsims) package, version 0.3.0, see the [documentation](https://mapsims.readthedocs.io/en/1.0.dev)

## Performance

At 4096 with lmax to `2*nside` **all 6 frequency channels**: 115 minutes for synchrotron and dust, 95 minutes for and ame, single node on Popeye (SDSC)
At 4096 with lmax to `3*nside` **each frequency channel** (e.g. `LA_27`, `SA_27`): 75 minutes for synchrotron and dust, 60 minutes for and ame, single node on Popeye (SDSC)
