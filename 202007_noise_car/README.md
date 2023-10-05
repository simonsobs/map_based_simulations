Realistic noise version 3.1.1 with MSS1 hitmaps in CAR pixelization
===================================================================

Tag: `mbs-s0012-20200722`

Release date 22 Jul 2020

For documentation refer to the [`202006_noise` release](https://github.com/simonsobs/map_based_simulations/tree/master/202006_noise)

The resolution of the CAR maps is defined in the [`so_default_resolution.  
csv` file](https://github.com/simonsobs/mapsims/blob/2.3.1/mapsims/data/so_default_resolution.csv)

For generating realizations on the fly, you can also check the [`mapsims_tutorials` notebooks](https://github.com/simonsobs/mapsims_tutorials)

## Available maps

Only 1 realizations of the full mission and 1 realization of 4 splits are made available as maps.

Reference frame for noise maps is assumed to be **Equatorial**.

**Location at NERSC**:

    /project/projectdirs/sobs/v4_sims/mbs/202007_noise_car

The naming convention is:

    {num:04d}/simonsobs_{content}_uKCMB_{tube}_{band}_CAR_{num:04d}_{split}_of_{nsplits}.fits"

where:

* `content` is `noise`
* `num` is the realization number (seed) and currently only `0`
* `tube` is `LT0`-`LT6` or `ST0`-`ST3`
* `band` is one of the available bandpasses:

        bands = ("LF1", "LF2", "MFF1", "MFF2", "MFS1", "MFS2", "UHF1", "UHF2")
        frequencies = (27, 39, 93, 145, 93, 145, 225, 280)

* `nsplits` is the number of splits, 1 for full mission, 4 for the splits, `split` is 1 based split ID.

For example: `0000/simonsobs_noise_uKCMB_ST2_MFS2_CAR_0000_1_of_1.fits`
