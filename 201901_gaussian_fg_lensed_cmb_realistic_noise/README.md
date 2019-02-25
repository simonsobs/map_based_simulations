Gaussian foregrouds, lensed CMB, realistic noise map based simulations
======================================================================

Release date 20 February 2019

The last version of this file is [available on Github](https://github.com/simonsobs/map_based_simulations/tree/master/201901_gaussian_fg_lensed_cmb_realistic_noise).
The same folder contains all the configuration files used and the scripts to create SLURM jobs.

## Input components

Each component is saved separately, all maps are in `uK_CMB`, IQU, single precision (`float32`)

* Gaussian synchrotron, see the [`GaussianSynchrotron` PySM component documentation](https://so-pysm-models.readthedocs.io/en/0.1.dev/models.html#gaussiansynchrotron) and the input parameters in `synchrotron.cfg`
* Gaussian dust, see the [`GaussianDust` PySM component documentation](https://so-pysm-models.readthedocs.io/en/0.1.dev/models.html#gaussiandust) and the input parameters in `dust.cfg`
* Lensed CMB, see the [`SOStandalonePrecomputedCMB` class in `mapsims`](https://mapsims.readthedocs.io/en/0.1.dev/api/mapsims.SOStandalonePrecomputedCMB.html#mapsims.SOStandalonePrecomputedCMB) and the [details about the CMB simulations](https://mapsims.readthedocs.io/en/0.1.dev/models.html#available-cosmic-microwave-background-simulations)
* Noise from power spectra released on 20180822, see [`SO_Noise_Calculator_Public_20180822.py`](https://github.com/simonsobs/mapsims/blob/0.1.0/mapsims/SO_Noise_Calculator_Public_20180822.py), the [`SONoiseSimulator` class in `mapsims`](https://mapsims.readthedocs.io/en/0.1.dev/models.html#noise-power-spectra-and-hitmaps).

## Available maps

HEALPix maps at high resolution (nside 4096), initially 10 realizations of all the input components

Low resolution maps just for channels of the Small Aperture telescopes, initially 100 realizations of noise and CMB, only 1 realization of Synchtron and Dust.

**Location at NERSC**:

    /project/projectdirs/sobs/v4_sims/mbs/201901_gaussian_fg_lensed_cmb_realistic_noise

The naming convention is:

    {output_nside}/{content}/{num:04d}/simonsobs_{content}_uKCMB_{telescope}{band:03d}_nside{nside}_{num:04d}.fits"

where:

* `content` is in `[cmb, synchtrotron, noise, dust]`
* `num` is `0`-`9` for high resolution simulations and `10`-`109` for low resolution simulations.
* `telescope` is `sa` or `la`
* `band` is the channel frequency in GHz

Total disk space used is 1.1 T for the 4096 simulations and 43 GB for the 512 simulations.

Backed up to tape in `~zonca/sobs/mbs/201901_gaussian_fg_lensed_cmb_realistic_noise`.

## Software

* The PySM components are available in the [`so_pysm_models`](https://github.com/simonsobs/so_pysm_models) package, version 0.1.0, see the [documentation](https://so-pysm-models.readthedocs.io/en/0.1.dev)
* The noise component and the runner script are available in the [`mapsims`](https://github.com/simonsobs/mapsims) package, version 0.1.0, see the [documentation](https://mapsims.readthedocs.io/en/0.1.dev)

## Benchmarks

Test runs of each component on 1 Cori Haswell node executing just 2 channels,
e.g. need to multiply the time by 6 to get the total for a full run.

In summary the 512 simulations are so quick and take so little memory we can run on `jupyter-dev`,
the 4096 foregrounds take ~140 minutes each, noise ~40 minutes, cmb ~15 minutes.

### 4096

cmb

* real    1m30.772s
* user    38m37.100s
* sys     4m17.152s

noise

* real    5m30.094s
* user    157m17.716s
* sys     7m36.576s

synchrotron

* real    22m10.193s
* user    1228m16.200s
* sys     8m19.556s

dust

* real    22m0.078s
* user    1215m13.356s
* sys     8m38.452s

### 512

noise

* real    0m10.580s
* user    2m0.508s
* sys     0m21.968s

synchrotron

* real    0m16.012s
* user    5m42.036s
* sys     0m39.224s

dust

* real    0m14.666s
* user    5m44.276s
* sys     0m37.572s

cmb

* real    0m19.171s
* user    6m1.800s
* sys     0m30.992s
