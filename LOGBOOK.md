# Map based simulations logbook

Date based updates from the map based simulation team

## 24 Apr 2020 - new noise simulations release `mbs-s0010-20200221` is broken

We fould out that the realistic noise simulations [`mbs-s0010-20200221`](202002_noise/README.md) are broken and should not be used, refer to their page for more details. We will need to rerun it.

## 20 Feb 2020 - Released new noise simulations

Released new noise simulation, partly as maps on disk (currently only 1 with splits) and partly to be simulated on the fly with the `mapsims` package. See <https://github.com/simonsobs/map_based_simulations/tree/master/202002_noise> for more details.
Discussion and feedback at <https://github.com/simonsobs/map_based_simulations/issues/21>

## 4 Dec 2019 - Overview of currently available simulations

Current the best full-sky signal simulations for the Simons Observatory are the tophat simulations [`mbs-s0006-20190705`](201906_highres_foregrounds_extragalactic_tophat/README.md),
they include galactic foregrounds, extragalactic and 1 CMB realization lensed and unlensed.
For more CMB realizations, lensed with gaussian potential instead of websky, see [`mbs-s0009-20191107`](201911_lensed_cmb/README.md).

For noise and sky coverage, [`mbs-s0007-20190618`](201906_noise_no_lowell/README.md) has 10 high resolution realizations and 100 
low resolution realization just for the SAT.
Consider that the hitmaps are quite old, new simulations are in the working see <https://github.com/simonsobs/map_based_simulations/issues/21>.

We also have Planck simulations, all the components in the SO tophat but for Planck delta-bandpasses: [`mbs-s0008-20190919`](201909_highres_foregrounds_extragalactic_planck_deltabandpass/README.md).
