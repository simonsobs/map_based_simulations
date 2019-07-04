Tophat bandpasses simulation: high resolution foregrounds with spectral index not varying spatially and extragalactic
=====================================================================================================================

Release date 5 July 2019

This is a re-run of the [`201903_highres_foregrounds`](https://github.com/simonsobs/map_based_simulations/tree/master/201903_highres_foregrounds) simulations in **Equatorial** coordinates instead of **Galactic**. The only other difference is that `hp.smoothing` now uses `use_pixel_weights=True`, i.e. the spherical harmonics transform should be of slightly better quality.

Also, this is the first set of simulations which uses the development version of [PySM 3](https://github.com/healpy/pysm).

The last version of this file is [available on Github](https://github.com/simonsobs/map_based_simulations/tree/master/201906_highres_foregrounds_extragalactic_tophat).
The same folder contains all the configuration files used and the scripts to create SLURM jobs.

## Input components

Each component is saved separately, all maps are in `uK_CMB`, IQU or I, single precision (`float32`)

Dust, synchrotron, free-free and anomalous microwave emission using the "0" models, i.e. `SO_d0`, `SO_s0`, `SO_f0`, and `SO_a0`, see more details in [in the documentation](https://so-pysm-models.readthedocs.io/en/latest/highres_templates.html#details-about-individual-models).

The CIB, KSZ and TSZ models are created from WebSky cosmological simulations, 
we also include one CMB realization generated with the same cosmological parameters used in the WebSky simulations both unlensed and lensed with the potential from the WebSky simulations,
see more details in [in the documentation](https://so-pysm-models.readthedocs.io/en/latest/models.html#websky).

## Instrument properties

Bandpass for each channel is based on the figures in `sotodlib`, PySM executes 10 equally spaced points between the low and the high limit, including both and integrates with the trapezoidal rule. Weighting is performed in `Jy/sr`, the same as PySM 2.
For the middle frequencies we have 2 possible bands which have slightly different bandpasses, therefore instead of tagging the maps by frequency, I use the band name.
Here is the table to link the band name to the reference frequencies, the actual center frequencies are available in `sotodlib`:

| Band | Reference freq [GHz] |
| ---- | -------------------- |
| LF1  | 27 |
| LF2  | 39 |
| MFF1 |  93 |
| MFF2 |  145 |
| MFS1 |  93 |
| MFS2 |  145 |
| UHF1 |  225 |
| UHF2 |  280 |

Beams are now read from `sotodlib`.

**Important notice about beams**: The beams used for all previous releases were read from `SO_Noise_Calculator_Public_20180822.py` and had obsolete values for SAT (in arcmin):

```
beam_SAT_27 = 91.
beam_SAT_39 = 63.
beam_SAT_93 = 30.
beam_SAT_145 = 17.
beam_SAT_225 = 11.
beam_SAT_280 = 9.
```

The new SAT beams are instead:

```
beam_SAT_27 = 144.
beam_SAT_39 = 99.
beam_SAT_93 = 42.
beam_SAT_145 = 27.
beam_SAT_225 = 19.
beam_SAT_280 = 17.
```

LAT beams are unchanged.

## Available maps

HEALPix maps at high resolution (nside 4096) and low resolution (nside 512), these models are deterministic, so we have
a set for each resolution for all channels.

Reference frame for the maps is **Equatorial**.
The `ell_max` for the harmonics transform is `3*Nside-1`.

**Location at NERSC**:

    /project/projectdirs/sobs/v4_sims/mbs/201906_highres_foregrounds_extragalactic_tophat

The naming convention is:

    {nside}/{content}/{num:04d}/simonsobs_{content}_uKCMB_{telescope}{band}_nside{nside}_{num:04d}.fits"

where:

* `content` is in `[dust, synchtrotron, freefree, ame]` for galactic components and `[ksz, tsz, cib]` for extragalactic components
* `content` for the available CMB is `[cmb, cmb_unlensed, cmb_lensed_solardipole]`, it is the same CMB realization, see the [WebSky documentation for details](https://so-pysm-models.readthedocs.io/en/latest/models.html#websky), `cmb` is the lensed version and `cmb_lensed_solardipole` is equal to `cmb` with the dipole component replaced by the [HFI 2018 solar dipole](https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/Map-making#HFI_2018_Solar_dipole)
* CIB map for LF1 is missing, see [issue on Github](https://github.com/simonsobs/map_based_simulations/issues/17)
* `num` is `0`
* `telescope` is `sa` or `la`
* `band` is the channel band, the options are: 

[TODO] backup to tape. Backed up to tape in `~zonca/sobs/mbs/201906_highres_foregrounds_extragalactic_tophat`.

## Galactic masks

See [The `201904_highres_foregrounds_equatorial` release](https://github.com/simonsobs/map_based_simulations/tree/master/201904_highres_foregrounds_equatorial)

## Issues or feedback

In case of any problem with the maps or the documentation or request more/different runs, [open an issue on the `map_based_simulations` repo](https://github.com/simonsobs/map_based_simulations/issues)

## Software

* The PySM components are available in the [`so_pysm_models`](https://github.com/simonsobs/so_pysm_models) package, version 2.0.0, see the [documentation](https://so-pysm-models.readthedocs.io/en/2.0.dev)
* The runner script is available in the [`mapsims`](https://github.com/simonsobs/mapsims) package, version 2.0.0, see the [documentation](https://mapsims.readthedocs.io/en/2.0.dev)
