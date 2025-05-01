# Map based simulation 19: WMAP Galactic, Extragalactic, CMB with bandpasses and beam window functions

Tag: `mbs-s0019-20250221`

## Updates

* 2025-04-30: Added `rg1`, `rg2` and `rg3` components, new combined maps with Radio Galaxies
* 2025-03-03: Completed verification and copied data to NERSC
* 2025-02-28: Executed simulation
* 2025-02-27: Created instrument model

## Summary

Full sky simulations for WMAP frequency channels of Galactic foregrounds using PySM 3 with the latest PySM models. Given that the main purpose of these simulations is to couple them with ground experiments, we simulate directly in Equatorial coordinates.

## Sky model

This release is based on the [3 sets of recommended sky models by the Panexperiment Galactic science group](https://galsci.github.io/blog/2022/common-fiducial-sky/), in summary:

* Low complexity `d9,s4,f1,a1,co1`
* Medium complexity `d10,s5,f1,a1,co3`
* High complexity `d12,s7,f1,a2,co3`

and based on Websky for extragalactic and CMB:

* `ksz1,tsz1`
* `c3`: CMB with same Cosmological parameters used in Websky unlensed
* `c4`: Same as `c3` but lensed by Websky

Documentation reference:

* `d9` `d10` GNILC based models and `d12` MKD 3D layered dust model: https://pysm3.readthedocs.io/en/latest/models.html#dust
* Synchrotron models `s4` and `s5`: https://pysm3.readthedocs.io/en/latest/models.html#synchrotron
* CO: https://pysm3.readthedocs.io/en/latest/models.html#co-line-emission
* All other Galactic models are the same of PySM 2: https://pysm3.readthedocs.io/en/latest/models.html
* For Extragalactic and CMB see [the PySM 3 documentation about Websky](https://pysm3.readthedocs.io/en/latest/websky.html#websky)

## Instrument model

See [`instrument_model.tbl`](instrument_model/instrument_model.tbl) for the instrument model, look into the [`instrument_model/extract_instrument_parameters.ipynb`](instrument_model/extract_instrument_parameters.ipynb) notebook to see how the instrument model was created.
WMAP released bandpasses in RJ units, therefore we divide them by $\nu^2$ to turn them into bandpasses in `MJy/sr` units [as expected by PySM](https://pysm3.readthedocs.io/en/latest/bandpass_integration.html). 

## Available maps

Maps are available in HEALPix pixelization.

Maps are in Equatorial Coordinates, `uK_CMB` units, FITS format.
See [`common.toml`](common.toml) for the naming convention.

Each of the components is available separately, see the TOML files in this repository for the configuration used to run PySM for each component.

The available combination maps are, (see the [`combine_maps.py` script](combine_maps.py)):

* `galactic_foregrounds_mediumcomplexity`
* `galactic_foregrounds_lowcomplexity`
* `galactic_foregrounds_highcomplexity`

And the related combined components includeing Websky extragalactic components, `cib1,tsz1,ksz1,rg2,rg3`, no CMB is included:

* `galactic_foregrounds_mediumcomplexity_websky`
* `galactic_foregrounds_lowcomplexity_websky`
* `galactic_foregrounds_highcomplexity_websky`

**Location at NERSC**, requires membership to the `cmb` group for access:

    /global/cfs/cdirs/cmb/gsharing/panexp_v1_wmap

The dataset is also available via [Globus](https://app.globus.org/file-manager?origin_id=53b2a147-ae9d-4bbf-9d18-3b46d133d4bb&origin_path=%2Fpanexp_v1_wmap%2F&two_pane=true)

Please [open an issue here](https://github.com/simonsobs/map_based_simulations/issues/new) for any data access problems.

## Model execution

Simulations were run using `mapsims 2.7.0a2` to coordinate the execution of `PySM 3.4.1a2`.
Given that each channel requested a different resolution, we have followed some guidelines, agreed with the Panexperiment Galactic science group:

* We have 2 resolution parameters, the output Nside is the requested resolution of the output map as defined in the instrument model. The modeling Nside instead is the resolution used to run PySM, then the output of PySM is transformed to Alm, beam-smoothed, rotated to Equatorial and anti-transformed to the output Nside. No `ud_grade` operations are ever performed.
* Evaluation of the PySM 3 models is executed at a minimum Nside 2048 or at the higher resolution available in the model. For example PySM 2 native models are executed at Nside 512, the new PySM 3 models are executed at 2048 even if we only want a Nside 128 output.
* Evaluation is executed at 2 times the requested output Nside, unless the requested output Nside is already the maximum available. For example if we request output at Nside 2048, `d10` is executed at 4096, if we request Nside 8192, `d10` is also executed at 8192.
* The maximum Ell is set to 2.5 times the lowest between the modeling and the output Nside, to avoid artifacts in the Spherical Harmonics transforms. Harmonics transforms are executed with [`hp.map2alm_lsq`](https://healpy.readthedocs.io/en/latest/generated/healpy.sphtfunc.map2alm_lsq.html) with 10 maximum iterations and 1e-7 target accuracy.
* This tecnique fails if the input templates have sharp features, in that case we use `ud_grade` to avoid ringing in the output maps. See [the issue in the PySM repository](https://github.com/galsci/pysm/issues/197)

## Verification

See [the README in the verification folder](verification/README.md)

## Known issues

* [Spikes in Synchrotron at high ell](https://github.com/CMB-S4/s4mapbasedsims/issues/29) if Galaxy is not masked. This should not affect much analysis, the galactic plane is always masked.

## Feedback

If anything looks even just suspicious in the simulations, please do not hesitate to [open an issue here](https://github.com/simonsobs/map_based_simulations/issues/new) and attach a Notebook to easily reproduce the problem.
