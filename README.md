Map based simulations for the Simons Observatory
================================================

Map based simulations for Simons Observatory, documentation about releases, maintained by the Map-Based Simulation Pipeline Working Group (MBS)

Slack channel: `#pwg-mbs`

## Available simulations

* [`mbs-s0012-20230321`](mbs-s0012-20230321/README.md): Galactic, extragalactic, CMB with realistic bandpasses.
* [`mbs-s0011-20200618`](202006_noise/README.md): Reran of realistic noise version 3.1.1 with MSS1 hitmaps
* [`mbs-s0009-20191107`](201911_lensed_cmb/README.md): 100 CMB realizations lensed with gaussian potential
* [`mbs-s0008-20190919`](201909_highres_foregrounds_extragalactic_planck_deltabandpass/README.md): Planck delta bandpasses: high resolution foregrounds with spectral index not varying spatially and extragalactic
* [`mbs-s0006-20190705`](201906_highres_foregrounds_extragalactic_tophat/README.md): Tophat bandpasses simulation: high resolution foregrounds with spectral index not varying spatially and extragalactic

## Logbook

Check [the Logbook](LOGBOOK.md) for the latest information about Map Based Simulations.

## Obsolete simulations

Data are now only stored on tape at NERSC under the `sobs` user. Please ask @zonca to recover them.

* [`mbs-s0010-20200221`](202002_noise/README.md): **Broken** Realistic noise version 3.1.1 with MSS1 hitmaps
* [`mbs-s0007-20190618`](201906_noise_no_lowell/README.md): Realistic noise with no power below ell 30
* [`mbs-s0005-20190520`](201905_extragalactic/README.md): Extragalactic emission with Websky
* [`mbs-s0004-20190610`](201904_highres_foregrounds_variable_spectral_index/README.md) High resolution foregrounds in Equatorial with spectral index varying spatially
* [`mbs-s0003-20190517`](201904_highres_foregrounds_equatorial/README.md): High resolution foregrounds in Equatorial with spectral index not varying spatially
* [`mbs-s0002-20190325`](201903_highres_foregrounds/README.md): High resolution foregrounds with spectral index not varying spatially
* [`mbs-s0001-20190220`](201901_gaussian_fg_lensed_cmb_realistic_noise/README.md): Gaussian foregrouds, lensed CMB, realistic noise map based simulations

## Maintained repositories

* [`mapsims`: Map-based simulation package based on PySM + SO noise simulations](https://github.com/galsci/mapsims)
* [`pysm`: Development version of PySM 3](https://github.com/galsci/pysm)
