Realistic noise with no power below ell 30
==========================================

Release date 18 June 2019

This is a re-run of the noise from the [`201901_gaussian_fg_lensed_cmb_realistic_noise` release](https://github.com/simonsobs/map_based_simulations/tree/master/201901_gaussian_fg_lensed_cmb_realistic_noise) but setting the noise power spectrum ell < 30 to zero.
This is based on the assessment on the [wiki, restricted](http://simonsobservatory.wdfiles.com/local--files/main%3Aawg-telecons/talk_AWG2?ukey=8e928be825a886291b1baa6b6b6d713714e8345d)


## Input components

Each component is saved separately, all maps are in `uK_CMB`, IQU, single precision (`float32`)

* Noise from power spectra released on 20180822, see [`SO_Noise_Calculator_Public_20180822.py`](https://github.com/simonsobs/mapsims/blob/0.1.0/mapsims/SO_Noise_Calculator_Public_20180822.py), the [`SONoiseSimulator` class in `mapsims`](https://mapsims.readthedocs.io/en/0.1.dev/models.html#noise-power-spectra-and-hitmaps).

## Available maps

HEALPix maps at high resolution (nside 4096), initially 10 realizations of all the input components

Reference frame for noise maps is **Equatorial**, Gaussian foregrounds and CMB have no intrinsic reference frame.
Bandpass for each channel is a delta function centered at the reference frequency.

Low resolution maps just for channels of the Small Aperture telescopes, initially 100 realizations of noise

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
