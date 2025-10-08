# Proposed plan: Updated version of MBS 16

See the [Documentation of MBS-16](https://github.com/simonsobs/map_based_simulations/blob/main/mbs-s0016-20241111/README.md).
Our initial plan is to update MBS-16 with the latest instrument model and add Half-Dome extragalactic components (on top of Websky), if available.

## Sky modelling

For Galactic components the plan is to use the Low, Medium and High Complexity sky models, the same we used in MBS-16, they are described in the Documentation of MBS-16 and in the [PySM methods paper](https://iopscience.iop.org/article/10.3847/1538-4357/adf212). Moreover, for comparison with previous simulations, we plan on running also the `s1` and `d1` models.

For Extragalactic components the plan is to use Websky 0.4, including the Catalog-based radio galaxy components. If available, we plan to release also all the Half-Dome components, so they are available for comparison.

For CMB, we will use the Websky 0.4 lensed and un-lensed components and possibly Half-Dome. We will also simulate separately the CMB Solar Dipole with frequency-varying quadrupole `dip2`.

## Bandpass

Realistic wafer-by-wafer bandpasses generated using the Bandpass Sampler (which will be included in PySM) starting from a reference bandpass based on the latest instrument model.

## Beam

The plan is to use Gaussian beams based on the most recently measured FWHM.

## Output maps

Output maps are both in CAR and HEALPix, with variable resolution by frequency,
using the same resolution used for real data.
Modelling is executed at twice the resolution and a minimum of NSIDE 2048,
in the final step, spherical harmonics are transformed to the target NSIDE or CAR resolution.
No intermediate maps are saved, only the final bandpass-integrated and beam-smoothed maps for each wafer.

We need to [check that the disk space occupied by the maps is reasonable](https://github.com/simonsobs/map_based_simulations/issues/71).

Available maps:

* Map of each individual component for each wafer (stored on tape and available upon request)
* Combined maps of Low, Medium and High Complexity Galactic emission for each wafer
* Combined maps `s1d1` Galactic emission for each wafer
* Combined Websky CMB + CMB Dipole for each wafer
* If available combined Half-Dome CMB + CMB Dipole for each wafer
* Combined Websky Extragalactic components
* If available, combined Half-Dome Extragalactic components

## Additional Data products

* Instrument model with all parameters used
* Configuration files used to run `mapsims`
