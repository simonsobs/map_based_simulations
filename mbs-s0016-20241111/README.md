# Map based simulation 16: Galactic, Extragalactic, CMB with realistic bandpasses by wafer

Tag: `mbs-s0016-20241111`

## TODO

* Run the new Websky Radio Galaxies Catalog-based components (`rg2` and `rg3`)
* Create new `extragalactic` combined map

## Updates

* 2025-02-10: Added SAT maps executed at 4096 to avoid sharp transitions in time domain due to large pixels, they are located in the `SAT_4096` subfolder of the release, also included the visual maps verification
* 2025-01-27: Executed spectra verification scripts
* 2025-01-18: Added `s1`, `d1`, and `galactic_foregrounds_d1s1` maps
* 2024-11-18: Finished map execution, also reconfigured `f1`, `a2` and `a1` to use `ud_grade` instead of spherical harmonics transforms to avoid ringing in the maps
* 2024-11-11: started map execution

## Summary

Full sky simulations for all Simons Observatory frequency channels for LAT and SAT of Galactic foregrounds using PySM 3 with the latest PySM models, using different bandpasses for each wafer simulated using [`bandpass_sampler`](https://github.com/simonsobs/bandpass_sampler/). 

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

See [`instrument_model.tbl`](instrument_model/instrument_model.tbl) for the instrument model, extracted from `sotodlib` and converted to IPAC table format, which has the advantage of supporting units for the columns and can be read as `astropy.QTable`.

```python
from astropy.table import QTable
instrument_model = QTable.read("instrument_model/instrument_model.tbl", format="ascii.ipac")
instrument_model.add_index("band")
```

Example on how to access all parameters for a band, or a specific one:

```python
instrument_model.loc["LAT_f030_w0"]
instrument_model.loc["LAT_f030_w0"]["fwhm"]
```

Simulated wafer by wafer bandpasses were generated by Giuseppe Puglisi, see the `bandpass_sampler` repository for more details, which is also included as a submodule in this repository.

```bash
git submodule update --init
```

## Available maps

Maps are available both in HEALPix and in CAR (Fejer1 variant) pixelizations, generated from the same set of Alms. The resolution of the maps varies by channel, all resolutions are available in the main instrument model table.

Maps are in Equatorial Coordinates, `uK_CMB` units, FITS format.
See [`common.toml`](common.toml) for the naming convention.

Each of the components is available separately, see the TOML files in this repository for the configuration used to run PySM for each component.

All components and combined maps for **SAT at nside 4096** are available in the subfolder `SAT_4096`.

The available combination maps are, (see the [`combine_maps.py` script](combine_maps.py)):

* `galactic_foregrounds_mediumcomplexity`
* `galactic_foregrounds_d1s1`
* `galactic_foregrounds_lowcomplexity`
* `galactic_foregrounds_highcomplexity`
* `extragalactic_norg_nocib` (Websky extragalactic maps without CIB and Radio Galaxies, so only kSZ and tSZ)

Radio Galaxies is not included yet, the new Catalog-based component still shows some issues, it will be released in the next weeks, the plan is to have 2 components, `rg2` for the sources > 1mJy generated on-the-fly directly at the target beam and resolution and `rg3`, interpolation-based componet for the fainter sources generated at a fiducial beam and differentially smoothed to the target beam.
Given we did not have Radio Galaxies, the analysis team recommended to exclude CIB for now, so that we have a set of simulations with no point sources.
Once available, we will release a new combined set `extragalactic` with all the 4 extragalactic components.

Which are meant to be used with either `cmb` for the Lensed CMB or with `cmb_unlensed`, the CMB maps have no solar dipole.

In case you only need 1 single set of maps with all the components, you should sum `galactic_foregrounds_mediumcomplexity`, `cmb` and `extragalactic_norg_nocib`.

**Location at NERSC**, this folder on the Simons Observatory project space only includes the combination maps and the 2 CMB maps (total of .75TB) due to space constraints:

    /global/cfs/cdirs/sobs/v4_sims/mbs/mbs-s0016-20241111

The entire release, including individual components are available on Perlmutter scratch (accessible from Perlmutter and from the Perlmutter JupyterHub node, it needs membership to the `sobs` group for read access):

    /pscratch/sd/z/zonca/mbs-s0016-20241111

Please [open an issue here](https://github.com/simonsobs/map_based_simulations/issues/new) for any data access problems.

## Metadata

Most useful metadata is available in the FITS header of the HEALPix maps, for example:

```
TTYPE1  = 'TEMPERATURE'                                                         
TFORM1  = '1024E   '                                                            
TUNIT1  = 'uK_CMB  '                                                            
TTYPE2  = 'Q_POLARISATION'                                                      
TFORM2  = '1024E   '                                                            
TUNIT2  = 'uK_CMB  '                                                            
TTYPE3  = 'U_POLARISATION'                                                      
TFORM3  = '1024E   '                                                            
TUNIT3  = 'uK_CMB  '                                                            
PIXTYPE = 'HEALPIX '           / HEALPIX pixelisation                           
ORDERING= 'NESTED  '           / Pixel ordering scheme, either RING or NESTED   
COORDSYS= 'C       '           / Ecliptic, Galactic or Celestial (equatorial)   
EXTNAME = 'xtension'           / name of this binary table extension            
NSIDE   =                 1024 / Resolution parameter of HEALPIX                
FIRSTPIX=                    0 / First pixel # (0 based)                        
LASTPIX =             12582911 / Last pixel # (0 based)                         
INDXSCHM= 'IMPLICIT'           / Indexing: IMPLICIT or EXPLICIT                 
OBJECT  = 'FULLSKY '           / Sky coverage, either FULLSKY or PARTIAL        
TELESCOP= 'SAT     '                                                            
BAND    = 'SAT_f290_w4'                                                         
TAG     = 'synchrotron_s4'                                                      
NUM     =                    0                                                  
ELL_MAX =                 2560                                                  
NSPLITS =                    1                                                  
SPLIT   =                    1                                                  
PYSMVERS= '3.4.1a1 '                                                            
```

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
