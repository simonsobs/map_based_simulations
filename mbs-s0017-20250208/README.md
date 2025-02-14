# Map based simulation 17: Planck Galactic, Extragalactic, CMB with bandpasses and beam window functions

Tag: `mbs-s0017-20250208`

## Updates

* 2025-02-08: Created instrument model from NPIPE products and Beyond Planck LFI bandpasses

## Summary

Full sky simulations for Planck frequency channels for HFI and LFI of Galactic foregrounds using PySM 3 with the latest PySM models. Given that the main purpose of these simulations is to couple them with ground experiments, we simulate directly in Equatorial coordinates.

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

See [`instrument_model.tbl`](instrument_model/instrument_model.tbl) for the instrument model, look into the [`instrument_model/extract_instrument_parameters.ipynb`](instrument_model/extract_instrument_parameters.ipynb) notebook to see how the instrument model was created. There are different conventions for the bandpasses in LFI and HFI.
All parameters come from NPIPE products which are based on the Planck 2018 data release, the LFI bandpasses are based on the Beyond Planck LFI bandpasses because remove some systematics effects present in the Planck bandpasses.

## Available maps

Maps are available both in HEALPix and in CAR (Fejer1 variant) pixelizations, generated from the same set of Alms. The resolution of the maps varies by channel, all resolutions are available in the main instrument model table.

Maps are in Equatorial Coordinates, `uK_CMB` units, FITS format.
See [`common.toml`](common.toml) for the naming convention.

Each of the components is available separately, see the TOML files in this repository for the configuration used to run PySM for each component.

The available combination maps are, (see the [`combine_maps.py` script](combine_maps.py)):

* `galactic_foregrounds_mediumcomplexity`
* `galactic_foregrounds_lowcomplexity`
* `galactic_foregrounds_highcomplexity`

Radio Galaxies is not included yet, the new Catalog-based component still shows some issues, it will be released in the future, the plan is to have 2 components, `rg2` for the sources > 1mJy generated on-the-fly directly at the target beam and resolution and `rg3`, interpolation-based componet for the fainter sources generated at a fiducial beam and differentially smoothed to the target beam.
Given we did not have Radio Galaxies, the analysis team recommended to exclude CIB for now, so that we have a set of simulations with no point sources.

**Location at NERSC**, requires membership to the `cmb` group for access:

    /global/cfs/cdirs/cmb/gsharing/panexp_v1_planck

The dataset is also available via [Globus](https://app.globus.org/file-manager?origin_id=53b2a147-ae9d-4bbf-9d18-3b46d133d4bb&origin_path=%2Fpanexp_v1_planck%2F&two_pane=true)

Please [open an issue here](https://github.com/simonsobs/map_based_simulations/issues/new) for any data access problems.

## Model execution

Simulations were run using `mapsims 2.7.0a1` to coordinate the execution of `PySM 3.4.1a1`.
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
