# Map based simulation 12: Galactic, Extragalactic, CMB with realistic bandpasses

Tag: `mbs-s0012-20230321`

## Updates

* 2023-03-21: first release

## Summary

Full sky simulations for all Simons Observatory frequency channels for LAT and SAT of Galactic foregrounds using PySM 3 with the new Dust and Synchrotron models, using realistic bandpasses instead of top-hat.

## Sky model

This release is based on the [3 sets of recommended sky models by the Panexperiment Galactic science group](https://galsci.github.io/blog/2022/common-fiducial-sky/), in summary:

* Low complexity `d9,s4,f1,a1,co1`
* Medium complexity `d10,s5,f1,a1,co3`
* High complexity `d12,s7,f1,a2,co3`

and based on Websky for extragalactic and CMB:

* `cib1,ksz1,tsz1,rg1`, `rg` stands Radio Galaxies.
* `c3`: CMB with same Cosmological parameters used in Websky unlensed
* `c4`: Same as `c3` but lensed by Websky

Documentation reference:

* `d9` `d10` GNILC based models and `d12` MKD 3D layered dust model: https://pysm3.readthedocs.io/en/latest/models.html#dust
* Synchrotron models `s4` and `s5`: https://pysm3.readthedocs.io/en/latest/models.html#synchrotron
* CO: https://pysm3.readthedocs.io/en/latest/models.html#co-line-emission
* All other Galactic models are the same of PySM 2: https://pysm3.readthedocs.io/en/latest/models.html
* For Extragalactic and CMB see [the PySM 3 documentation about Websky](https://pysm3.readthedocs.io/en/latest/websky.html#websky)

## Instrument model

See the `simonsobs_instrument_parameters_2023.03/` folder for test files which encode all the instrument model parameters extracted from `sotodlib` and the [notebook used to generate them](simonsobs_instrument_parameters_2023.03/extract_so_instrument_parameters.ipynb).

Realistic bandpasses from the [Instrument model](https://github.com/simonsobs/instrument_model/tree/master/instrument_hardware/modeled_bandpasses), see plots in the above-mentioned notebook.
Using the same configuration of the SO v3 sensitivity calculator:

* *LF*: On-chip bandpass filters
* *MF*: On-chip bandpass filters + Gain effects
* *UHF*: On-chip bandpass filters + Gain effects

## Available maps

Maps are available both in HEALPix and in CAR (Fejer1 variant) pixelizations, generated from the same set of Alms. The resolution of the maps varies by channel, all resolutions are available in the main instrument model table.

Maps are in Equatorial Coordinates, `uK_CMB` units, FITS format.
See [`common.toml`](common.toml) for the naming convention.

Each of the 17 components is available separately, see the TOML files in this repository for the configuration used to run PySM for each component.

The available combination maps are 4, (see the [`combine_maps.py` script](combine_maps.py)):

* `galactic_foregrounds_mediumcomplexity`
* `galactic_foregrounds_lowcomplexity`
* `galactic_foregrounds_highcomplexity`
* `extragalactic`

Which are meant to be used with either `cmb` for the Lensed CMB or with `cmb_unlensed`.

In case you only need 1 single set of maps with all the components, you should sum `galactic_foregrounds_mediumcomplexity`, `cmb` and `extragalactic`.

**Location at NERSC**, this folder on the Simons Observatory project space only includes the 4 combination maps and the 2 CMB maps (total of .75TB) due to space constraints:

    /project/projectdirs/sobs/v4_sims/mbs/mbs-s0012-20230321

Individual components (2.2 TB) are available on Cori scratch (accessible from Cori and from the Cori JupyterHub node, it needs membership to the `sobs` group for read access):

    /global/cscratch1/sd/zonca/mbs-s0012-20230321

Please [open an issue here](https://github.com/galsci/pysm/issues/new) for any data access problems.

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
BAND    = 'SAT_f230'                                                            
TAG     = 'synchrotron'                                                         
NUM     =                    0                                                  
ELL_MAX =                 2560                                                  
NSPLITS =                    1                                                  
SPLIT   =                    1                                                  
```

## Model execution

Simulations were run using `mapsims 2.6.0` to coordinate the execution of `PySM 3.4.0b8`.
Given that each channel requested a different resolution, we have followed some guidelines, agreed with the Panexperiment Galactic science group:

* We have 2 resolution parameters, the output Nside is the requested resolution of the output map as defined in the instrument model. The modeling Nside instead is the resolution used to run PySM, then the output of PySM is transformed to Alm, beam-smoothed, rotated to Equatorial and anti-transformed to the output Nside. No `ud_grade` operations are ever performed.
* Evaluation of the PySM 3 models is executed at a minimum Nside 2048 or at the higher resolution available in the model. For example PySM 2 native models are executed at Nside 512, the new PySM 3 models are executed at 2048 even if we only want a Nside 128 output.
* Evaluation is executed at 2 times the requested output Nside, unless the requested output Nside is already the maximum available. For example if we request output at Nside 2048, `d10` is executed at 4096, if we request Nside 8192, `d10` is also executed at 8192.
* The maximum Ell is set to 2.5 times the lowest between the modeling and the output Nside, to avoid artifacts in the Spherical Harmonics transforms. Harmonics transforms are executed with [`hp.map2alm_lsq`](https://healpy.readthedocs.io/en/latest/generated/healpy.sphtfunc.map2alm_lsq.html) with 10 maximum iterations and 1e-7 target accuracy.

## Verification

Interactive power spectra plots for all components except CO and radio galaxies, the source notebook is available in the `verification/` folder:

* [SAT TT](https://nbviewer.org/gist/zonca/3645fe8042c7d913213f3dbd647be0d5)
* [LAT TT](https://nbviewer.org/gist/zonca/7026e5f4fd9ef304a89f1c171e43f2ce)
* [SAT EE](https://nbviewer.org/gist/zonca/612defba6ad8d4137781661cda110bd9)
* [LAT EE](https://nbviewer.org/gist/zonca/242527ea6bc1bc67085a7f2ae480e2df)
* [SAT BB](https://nbviewer.org/gist/zonca/c08d6bcdd5b920b459eac77256c1d36b)
* [LAT BB](https://nbviewer.org/gist/zonca/e9f3eebb8304583f9874cd61da95aeed)

## Known issues

* Websky Radio sources are available only down to 18.7 GHz, the lowest Simons Observatory channels have bandpasses to 10 Ghz, so I created a copy of 18.7 GHz and renamed it to 1.0 GHz. This is the border of the band, should not matter much.

## Feedback

If anything looks even just suspicious in the simulations, please do not hesitate to [open an issue here](https://github.com/galsci/pysm/issues/new) and attach a Notebook to easily reproduce the problem.
