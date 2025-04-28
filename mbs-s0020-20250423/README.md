# Map based simulation 20: BK18 Galactic, Extragalactic, CMB with measured bandpasses and gaussian beams

Tag: `mbs-s0020-20250423`

## Updates

* 2025-02-28: Maps copied to NERSC
* 2025-04-24: Maps executed on Popeye
* 2025-04-23: Created instrument model

## Summary

Full sky simulations for Bicep Keck channels of Galactic foregrounds using PySM 3 with the latest PySM models.

## Sky model

This release is based on the [3 sets of recommended sky models by the Panexperiment Galactic science group](https://galsci.github.io/blog/2022/common-fiducial-sky/), in summary:

* Low complexity `d9,s4,f1,a1,co1`
* Medium complexity `d10,s5,f1,a1,co3`
* High complexity `d12,s7,f1,a2,co3`

and based on Websky for extragalactic and CMB:

* `ksz1,tsz1,cib1`
* `rg2,rg3`: catalog-based radio galaxies components
* `c3`: CMB with same Cosmological parameters used in Websky unlensed
* `c4`: Same as `c3` but lensed by Websky

Documentation reference:

* `d9` `d10` GNILC based models and `d12` MKD 3D layered dust model: https://pysm3.readthedocs.io/en/latest/models.html#dust
* Synchrotron models `s4` and `s5`: https://pysm3.readthedocs.io/en/latest/models.html#synchrotron
* CO: https://pysm3.readthedocs.io/en/latest/models.html#co-line-emission
* All other Galactic models are the same of PySM 2: https://pysm3.readthedocs.io/en/latest/models.html
* For Extragalactic and CMB see [the PySM 3 documentation about Websky](https://pysm3.readthedocs.io/en/latest/websky.html#websky)

## Instrument model

We are using Gaussian beams and measured bandpasses as released by the Bicep Keck collaboration.
The instrument model details can be found in [`instrument_model.tbl`](instrument_model/instrument_model.tbl). For information on how this model was constructed, refer to the notebook [`extract_instrument_parameters.ipynb`](instrument_model/extract_instrument_parameters.ipynb) within the same directory.

## Available maps

Maps are available in HEALPix pixelization.

Maps are in Equatorial Coordinates, `uK_CMB` units, FITS format.
See [`common.toml`](common.toml) for the naming convention.

Each of the components is available separately, see the TOML files in this repository for the configuration used to run PySM for each component.

The available combination maps are, (see the [`combine_maps.py` script](combine_maps.py)), for only galactic components:

* `galactic_foregrounds_mediumcomplexity`
* `galactic_foregrounds_lowcomplexity`
* `galactic_foregrounds_highcomplexity`

And the related combined components includeing Websky extragalactic components, `cib1,tsz1,ksz1,rg2,rg3`, no CMB is included:

* `galactic_foregrounds_mediumcomplexity_websky`
* `galactic_foregrounds_lowcomplexity_websky`
* `galactic_foregrounds_highcomplexity_websky`

**Location at NERSC**, requires membership to the `cmb` group for access:

    /global/cfs/cdirs/cmb/gsharing/panexp_v1_bk18

The dataset is also available via [Globus](https://app.globus.org/file-manager?origin_id=53b2a147-ae9d-4bbf-9d18-3b46d133d4bb&origin_path=%2Fpanexp_v1_bk18%2F&two_pane=true)

Please [open an issue here](https://github.com/simonsobs/map_based_simulations/issues/new) for any data access problems.

## Model execution

Simulations were run using `mapsims 2.7.0` to coordinate the execution of `PySM 3.4.1`.

* Evaluation of the PySM 3 models is executed at a minimum Nside 2048 or at the higher resolution available in the model. For example PySM 2 native models are executed at Nside 512, the new PySM 3 models are executed at 2048 even if we only want a lower resolution output.
* Evaluation is executed at 2 times the requested output Nside, unless the requested output Nside is already the maximum available. For example if we request output at Nside 2048, `d10` is executed at 4096, if we request Nside 8192, `d10` is also executed at 8192.
* The maximum Ell is set to 2.5 times the lowest between the modeling and the output Nside, to avoid artifacts in the Spherical Harmonics transforms. Harmonics transforms are executed with [`hp.map2alm_lsq`](https://healpy.readthedocs.io/en/latest/generated/healpy.sphtfunc.map2alm_lsq.html) with 10 maximum iterations and 1e-7 target accuracy.
* This tecnique fails if the input templates have sharp features, in that case we use `ud_grade` to avoid ringing in the output maps. See [the issue in the PySM repository](https://github.com/galsci/pysm/issues/197)

## Verification

See [the README in the verification folder](verification/README.md)

## Known issues

* [Spikes in Synchrotron at high ell](https://github.com/CMB-S4/s4mapbasedsims/issues/29) if Galaxy is not masked. This should not affect much analysis, the galactic plane is always masked.

## Feedback

If anything looks even just suspicious in the simulations, please do not hesitate to [open an issue here](https://github.com/simonsobs/map_based_simulations/issues/new) and attach a Notebook to easily reproduce the problem.