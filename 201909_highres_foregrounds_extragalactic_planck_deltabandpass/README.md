Planck delta bandpasses: high resolution foregrounds with spectral index not varying spatially and extragalactic
=====================================================================================================================

Tag: `mbs-s0008-20190919`

Released on 19 September 2019 by @zonca

Planck frequency channels with Dirac delta bandpasses and gaussian beams, extracted from the [Planck instrument models for the 2018 release](https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/The_RIMO). See the `planck_deltabandpass.h5` file in the `data` folder of the `mapsims` package at: <https://github.com/simonsobs/mapsims/blob/master/mapsims/data/planck_deltabandpass.h5>.
Example:

    In [1]: import h5py
    In [2]: f = h5py.File("planck_deltabandpass.h5")

    In [3]: f.keys()
    Out[3]: <KeysViewHDF5 ['030', '044', '070', '100', '143', '217', '353', '545', '857']>

    In [4]: f["143"].attrs
    Out[4]: <Attributes of HDF5 object at 46913457708992>

    In [5]: list(f["143"].attrs)
    Out[5]: ['band', 'center_frequency_GHz', 'fwhm_arcmin']

    In [6]: f["143"].attrs["center_frequency_GHz"]
    Out[6]: 142.876

It includes all galactic high resolution components with index not varying spatially and the extragalactic
components based on WebSky.

The last version of this file is [available on Github](https://github.com/simonsobs/map_based_simulations/tree/master/201909_highres_foregrounds_extragalactic_planck_deltabandpass).
The same folder contains all the configuration files used and the scripts to create SLURM jobs.

## Input components

Each component is saved separately, all maps are in `uK_CMB`, IQU or I, single precision (`float32`)

Dust, synchrotron, free-free and anomalous microwave emission using the "0" models, i.e. `SO_d0`, `SO_s0`, `SO_f0`, and `SO_a0`, see more details in [in the documentation](https://so-pysm-models.readthedocs.io/en/latest/highres_templates.html#details-about-individual-models).

The CIB, KSZ and TSZ models are created from WebSky cosmological simulations,
we also include one CMB realization generated with the same cosmological parameters used in the WebSky simulations both unlensed and lensed with the potential from the WebSky simulations,
see more details in [in the documentation](https://so-pysm-models.readthedocs.io/en/latest/models.html#websky).

## Available maps

HEALPix maps at high resolution (nside 4096) and low resolution (nside 512), these models are deterministic, so we have
a set for each resolution for all channels. All maps are full-sky.

Reference frame for the maps is **Equatorial**.
The `ell_max` for the harmonics transform is `3*Nside-1`.

**Location at NERSC**:

    /project/projectdirs/sobs/v4_sims/mbs/201909_highres_foregrounds_extragalactic_planck_deltabandpass

The naming convention is:

    {nside}/{content}/{num:04d}/planck_deltabandpass_{content}_uKCMB_{telescope}{band:0<3}_nside{nside}_{num:04d}.fits"

where:

* `content` is `[dust, synchtrotron, freefree, ame]` for galactic components and `[ksz, tsz, cib]` for extragalactic components
* `content` for the available CMB is `[cmb, cmb_unlensed]`
* `num` is `0`
* `telescope` is `planck`
* `band` is the channel band, the options are: `030,044,070,100,143,217,353,545,857`

**NOTE** on CIB: CIB templates are available only up to 857 GHz, but the highest Planck channel frequency is actually 866.8 GHz, so just for CIB I reduced the center frequency of this channel to 857 GHz.

Backed up to tape in `~zonca/sobs/mbs/201909_highres_foregrounds_extragalactic_planck_deltabandpass`.

## Combined maps

Also created a single set of maps which is the sum of all components (for CMB `cmb`, which is the lensed version). 
They are in the same folder and same naming convention with `content` equal to `combined`, e.g.:

    /global/project/projectdirs/sobs/v4_sims/mbs/201909_highres_foregrounds_extragalactic_planck_deltabandpass/4096/combined/0000/planck_deltabandpass_combined_uKCMB_planck070_nside4096_0000.fits

## Plots of power spectra

You can also download the notebooks, update paths and modify them:

* [nside 512 input maps](https://nbviewer.jupyter.org/gist/zonca/237fde577156076288bbec923e5b748e), get notebook from [this gist](https://gist.github.com/zonca/237fde577156076288bbec923e5b748e)
* [images for the NSIDE 4096 maps](https://github.com/simonsobs/map_based_simulations/issues/24#issuecomment-535545595), produced from the same notebook above accessing the NSIDE 4096 maps instead of the NSIDE 512 ones.

## Galactic masks

See [The `201904_highres_foregrounds_equatorial` release](https://github.com/simonsobs/map_based_simulations/tree/master/201904_highres_foregrounds_equatorial)

## Issues or feedback

In case of any problem with the maps or the documentation or request more/different runs, [open an issue on the `map_based_simulations` repo](https://github.com/simonsobs/map_based_simulations/issues)

## Software

* PySM 3 is available at <https://github.com/healpy/pysm>, version 3.0.0
* [`sotodlib`](https://github.com/simonsobs/sotodlib) commit [`aca85843b70`](https://github.com/simonsobs/sotodlib/commit/aca85843b70b0c6ebac031aa48fff47f93ed6661) 
* The PySM components are available in the [`so_pysm_models`](https://github.com/simonsobs/so_pysm_models) package, version 2.0.0, see the [documentation](https://so-pysm-models.readthedocs.io/en/2.0.dev)
* The runner script is available in the [`mapsims`](https://github.com/simonsobs/mapsims) package, version 2.0.0, see the [documentation](https://mapsims.readthedocs.io/en/2.0.dev)
