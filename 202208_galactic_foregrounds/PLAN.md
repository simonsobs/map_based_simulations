Foreground simulation with realistic bandpasses and new Dust/Synchrotron models
===============================================================================

Produce full sky simulations of Galactic foregrounds using PySM 3 with the new Dust and Synchrotron models, using realistic bandpasses instead of top-hat.
CMB and Extragalactic will be in a future release, [waiting for the new run of Websky](https://github.com/galsci/pysm/issues/120)

## Foreground models

The plan is to run 3 different sky models, optimistic/baseline/pessimistic, see the discussion in [this PySM 3 issue](https://github.com/galsci/pysm/issues/103#issuecomment-1081241879), for convenience here the 3 sets of models:

1. `optimistic`: d9,s4,f1,a1,co1
2. `bestguess`: d10,s5,f1,a1,co3
3. `pessimistic`: d12,s7,f1,a2,co3

Documentation reference:

* `d9` `d10` GNILC based models and `d12` MKD 3D layered dust model: https://pysm3.readthedocs.io/en/latest/models.html#dust
* Synchrotron models `s4` and `s5`: https://pysm3.readthedocs.io/en/latest/models.html#synchrotron
* CO: https://pysm3.readthedocs.io/en/latest/models.html#co-line-emission
* All other models are the same of PySM 2: https://pysm3.readthedocs.io/en/latest/models.html

There are 2 issues:

### Rotation to Equatorial

In previous runs I had created Equatorial versions of all the templates to avoid having to rotate the maps because it was not supported by libsharp, for this release we can stop using libsharp and instead use all the Galactic templates and then rotate to Equatorial at the last step when we are in spherical harmonics space for smoothing.

### Low resolution models

* d9, d10, s4, s5 and s7 are available up to 8192
* d12 to 2048
* f1, a1, a2 to 512, however we have an extrapolation to 4096 by @NicolettaK, see <https://portal.nersc.gov/project/cmb/so_pysm_models_data/>
* co? to 512 (2048 are available, but maps are smoothed at 1 deg anyway)

I suggest to not use the extrapolated map by @NicolettaK, because they use a different method from the new Dust and Synchrotron models. We plan in the future to have AME and Free-free maps at 8192 with small scales produced in a similar fashion to the `d10`/`s5` models.

I would run the maps in PySM at `min(max(2048, 2*Nside), available_resolution)`, then in the smoothing process, we can do a `alm2map` at the target resolution.
Never use `hp.ud_grade`.

## Bandpasses

Use bandpasses from the [Instrument model](https://github.com/simonsobs/instrument_model/tree/master/instrument_hardware/modeled_bandpasses)

Using the same configuration of the SO v3 sensitivity calculator:

* *LF*: On-chip bandpass filters
* *MF*: On-chip bandpass filters + Gain effects
* *UHF*: On-chip bandpass filters + Gain effects

Will be reformatted and added to instrument model in text format like: <https://github.com/simonsobs/mapsims/tree/master/mapsims/data/simonsobs_instrument_parameters_2020.06>

## Beams

Will be extracted from `sotodlib` into a table in txt format and added to `mapsims`, like [`simonsobs_instrument_parameters_2020.06.tbl`](https://github.com/simonsobs/mapsims/blob/master/mapsims/data/simonsobs_instrument_parameters_2020.06/simonsobs_instrument_parameters_2020.06.tbl) in the last release.

## Pixelization

Ideally we want to produce in 1 run only both HEALPix and CAR, once we have alms of the output map in equatorial, we can produce both final output HEALPix and CAR.

Need to implement this into `mapsims`.

Variable Nside: <https://github.com/simonsobs/mapsims/blob/master/mapsims/data/so_default_resolution.csv>

Using `ell_max = 3 Nside - 1`, write in the FITS headers the actual `ell_max` and `Nside` used for modelling.

## Output files

FITS files, full sky, Equatorial, `uK_CMB`, always IQU, even if component is I only to avoid broadcasting mistakes, single precision (float32), for HEALPix RING ordering.
[Add more metadata to FITS headers](https://github.com/simonsobs/map_based_simulations/issues/38)

1 map saved in FITS format for each:

* sky model (optimistic, bestguess, pessimistic)
* sky component (dust, synchrotron, free-free, CO - only if present in band, AME, their sum)
* frequency channel (6 LAT, 6 SAT)
* pixelization (HEALPix and CAR)

Total 3 * 6 * 12 * 2 = 432 maps

Naming conventions, is there any standard SO naming convention we should follow?
Otherwise we can use the [same used for the last noise simulation](https://github.com/simonsobs/map_based_simulations/tree/master/202006_noise#available-maps)
