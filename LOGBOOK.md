# Map based simulations logbook

Date based updates from the map based simulation team

## 8 July 2024 - Released LAT map-based noise simulations

Based on the LAT time-domain ``mss0002`` mission scale simulations, using the directional wavelet noise model of [`mnms`](https://github.com/simonsobs/mnms).

## 20 Sep 2023 - Released realistic SAT map-based noise simulations

Based on the SAT time-domain ``mbs-noise-sims-sat`` simulations, using the tiled noise model of [`mnms`](https://github.com/simonsobs/mnms).

## 9 May 2023 - Released realistic LAT map-based noise simulations

Based on the LAT time-domain `scan-s0003` simulations, using the directional wavelet noise model of [`mnms`](https://github.com/simonsobs/mnms).

## 21 March 2023 - Released MBS simulation 12

Galactic, extragalactic and CMB with realistic bandpasses.
For noise simulations, see <https://github.com/simonsobs/mnms>

## 18 Jun 2020 - Released fixed noise simulation

Released new noise simulation, partly as maps on disk (currently only 1 with splits) and partly to be simulated on the fly with the `mapsims` package. See <https://github.com/simonsobs/map_based_simulations/tree/master/202006_noise> for more details.

## 2 Jun 2020 - CMB tensor modes from websky

BB spectrum compatible with WebSky is available, see https://so-pysm-models.readthedocs.io/en/latest/models.html#websky

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
