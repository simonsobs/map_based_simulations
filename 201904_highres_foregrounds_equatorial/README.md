High resolution foregrounds in Equatorial with spectral index not varying spatially
===================================================================================

Release date 17 May 2019

This is a re-run of the [`201903_highres_foregrounds`](https://github.com/simonsobs/map_based_simulations/tree/master/201903_highres_foregrounds) simulations in **Equatorial** coordinates instead of **Galactic**. The only other difference is that `hp.smoothing` now uses `use_pixel_weights=True`, i.e. the spherical harmonics transform should be of slightly better quality.

Also, this is the first set of simulations which uses the development version of [PySM 3](https://github.com/healpy/pysm).

The last version of this file is [available on Github](https://github.com/simonsobs/map_based_simulations/tree/master/201904_highres_foregrounds_equatorial).
The same folder contains all the configuration files used and the scripts to create SLURM jobs.

## Input components

Each component is saved separately, all maps are in `uK_CMB`, IQU or I, single precision (`float32`)

Dust, synchrotron, free-free and anomalous microwave emission using the "0" models, i.e. `SO_d0`, `SO_s0`, `SO_f0`, and `SO_a0`, see more details in [in the documentation](https://so-pysm-models.readthedocs.io/en/latest/highres_templates.html#details-about-individual-models).

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

    /project/projectdirs/sobs/v4_sims/mbs/201904_highres_foregrounds_equatorial

The naming convention is:

    {output_nside}/{content}/{num:04d}/simonsobs_{content}_uKCMB_{telescope}{band:03d}_nside{nside}_{num:04d}.fits"

where:

* `content` is in `[cmb, synchtrotron, freefree, ame]`
* `num` is `0`
* `telescope` is `sa` or `la`
* `band` is the channel frequency in GHz

Backed up to tape in `~zonca/sobs/mbs/201904_highres_foregrounds_equatorial`.

## Available Galactic masks

In Equatorial coordinates

    /project/projectdirs/sobs/v4_sims/mbs/201904_highres_foregrounds_equatorial/{output_nside}/masks
    
Masks are optimized for polarization.

They are generate comparing synchrotron+dust polarized signal at 93 GHz with the CMB standard deviation at one degree angular resolution.

Sky is masked wherever:
    `abs(FG_Q) > thr * std(CMB_Q)` 
or 
    `abs(FG_U) > thr * std(CMB_U)`

the obtained masks are further smoothed with a gaussian kernel at 10 degree in order to get regular mask edges.
The `thr` parameter ranges from `1` to `4.5`. The final masks cover a fraction of the sky (evaluated over the full sky) between `0.28`and `0.75`

## Issues or feedback

In case of any problem with the maps or the documentation or request more/different runs, [open an issue on the `map_based_simulations` repo](https://github.com/simonsobs/map_based_simulations/issues)

## Plots

See the `plot_maps.ipynb` notebook in the folder, executed notebooks:

* [NSIDE 512](https://gist.github.com/e2a4c5d04cb12800318f753e0e5a8c4d)
* [NSIDE 4096](https://gist.github.com/a42219fdf3fc611071078ee010e90a43)

## Software

* The PySM components are available in the [`so_pysm_models`](https://github.com/simonsobs/so_pysm_models) package, version 1.0.0, see the [documentation](https://so-pysm-models.readthedocs.io/en/latest)
* The noise component and the runner script are available in the [`mapsims`](https://github.com/simonsobs/mapsims) package, version 0.3.0, see the [documentation](https://mapsims.readthedocs.io/en/latest)

## Performance

At 4096 with lmax to `2*nside` **all 6 frequency channels**: 115 minutes for synchrotron and dust, 95 minutes for freefree and ame, single node on Popeye (SDSC)

At 4096 with lmax to `3*nside-1` **each frequency channel** (e.g. `LA_27`, `SA_27`): 75 minutes for synchrotron and dust, 60 minutes for freefree and ame, single node on Popeye (SDSC)
