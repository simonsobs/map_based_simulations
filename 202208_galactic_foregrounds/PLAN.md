Foreground simulation with realistic bandpasses and new Dust/Synchrotron models
===============================================================================

## Foreground models

The plan is to run 3 different sky models, optimistic/baseline/pessimistic, see the discussion in [this PySM 3 issue](https://github.com/galsci/pysm/issues/103#issuecomment-1081241879), for convenience here the 3 sets of models:

1. d9,s4,f1,a1,co1
2. d10,s5,f1,a1,co3
3. d12,s7,f1,a2,co3

### Rotation to Equatorial

There are 2 issues, in previous runs I had created Equatorial versions of all the templates to avoid having to rotate the maps because it was not supported by libsharp, for this release we can stop using libsharp and instead use all the Galactic templates and then rotate to Equatorial at the last step when we are in spherical harmonics space for smoothing.

### Low resolution models

* d9, d10, s4, s5 and s7 are available up to 8192
* d12 to 2048
* f1, a1, a2 to 512, however we have an extrapolation to 4096 by @NicolettaK, see <https://portal.nersc.gov/project/cmb/so_pysm_models_data/equatorial/>
* co? to ??
