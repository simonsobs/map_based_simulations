# Map-based noise simulations based on the LAT `mss-0002` mission-scale time-domain simulations

Tag: `mbs-s0015-20240504`

## Updates

* 2024-06-10: first release, `lmax=5400` simulations.

## Summary

300 realistic realizations of the LAT map noise, given the single realization of the time-domain simulations. Simulations cover the full LAT footprint to a bandlimit of `lmax=5400`, and utilize the directional wavelet noise model.

## Noise model

This release is based on the LAT `mss-0002` time-domain simulations, available on `NERSC` at:

    /global/cfs/cdirs/sobs/sims/mss-0002/RC1.r01

These time-domain simulations provide four noise splits for each frequency band. More information is available on the SO [productdb](https://www.productdb.simonsobservatory.org/product/simulation/mss-0002).

Using [`mnms`](https://github.com/simonsobs/mnms), we generate 300 realizations of the noise using map-based methods. Specifically, we use the directional wavelet model, governed by the configured [parameters](parameters/so_lat_mbs_mss0002.yaml).

Notes:
* Simulations are bandlimited to `lmax=5400`. To save space, the simulations for the f090, f150, f230 and f280 bands are stored in a pixelization that is downgraded by a factor of 4 relative to the time-domain simulations (no downgrading was needed for the f030 and f040 maps) (`shape=(..., 2640, 10800)`, 2 arcmin resolution vs. `shape=(..., 10560, 43200)` 0.5 arcmin resolution). See [examples](#example-usage) below for further guidance.
* The following releases were used: [`mnms v0.0.7`](https://github.com/simonsobs/mnms/tree/v0.0.7) and [`sofind v0.0.5`](https://github.com/simonsobs/sofind/tree/v0.0.5)
* A mask has been applied to the map-domain simulations that removes a small amount of noisy pixels at the edges of the maps. The masks are stored here: `/global/cfs/cdirs/sobs/v4_sims/mbs/mbs_s0015_20240504/masks/LAT_{bands}_mask_obs.fits`.
* See these [slides](https://drive.google.com/file/d/1ua8AmFIUonuAgn67LnM8IgIHIxONSawP/view?usp=sharing) for validation of the map-based simulations.

## Available maps

Maps are available in the CAR (Fejer1 variant) pixelization. As above, the maps have a resolution of 2 arcmin. Maps are in Equatorial Coordinates, `uK_CMB` units, FITS format.

The maps are located here:

    /global/cfs/cdirs/sobs/v4_sims/mbs/mbs_s0015_20240504/sims

and have the following naming convention:

    so_lat_mbs_mss0002_fdw_{bands}_lmax5400_4way_set{split_num}_noise_sim_map{sim_num:04}.fits

where `bands` is in `[lf_f030_lf_f040, mf_f090_mf_f150, uhf_f230_uhf_f290]`, `split_num` is in `[0-3]` and `sim_num` is in `[0000-0299]`.

The simulations take up 2.3 TB.

Please [open an issue here](https://github.com/simonsobs/map_based_simulations/issues/new) for any data access problems.

## Available models

The covariance matrices from which simulations are drawn are available here: 

    /global/cfs/cdirs/sobs/v4_sims/mbs/mbs_s0015_20240504/models

The `/global/cfs/cdirs/sobs/v4_sims/mbs/mbs_s0015_20240504/renamed` directory contains ancillary map files needed to draw from the covariance matrices or to generate new matrices. See the [preprocess_maps.py](https://github.com/simonsobs/map_based_simulations/blob/master/mbs-s0015-20240504/preprocess_maps.py) script to see how these files were generated.

## Metadata

The models correlate pairs of frequency bands on the same detector wafer. Therefore, the simulations are stored in a similar paired format. Thus, the shape of a given simulation file is `(2, 1, 3, 2640, 10800)`:
* The first axis is the frequency band
* The second (singleton) axis follows `mnms` convention (reserved for map splits; since each simulation corresponds to one map split, the dimension of this axis is 1)
* The third axis is Stokes component (I, Q, U)
* The last axes are the map pixels

The geometry (including shape) of the maps is given in the FITS header:
```
SIMPLE  =                    T / conforms to FITS standard                      
BITPIX  =                  -32 / array data type                                
NAXIS   =
 5 / number of array dimensions                     
NAXIS1  =                10800                                                  
NAXIS2  =                 2640
NAXIS3  =                    3                                                  
NAXIS4  =                    1                                                  
NAXIS5  =                    2                                                  
WCSAXES =                    2 / Number of coordinate axes                      
CRPIX1  =               5401.0 / Pixel coordinate of reference point            
CRPIX2  =               1890.5 / Pixel coordinate of reference point            
CDELT1  =   -0.033333333333333 / [deg] Coordinate increment at reference point  
CDELT2  =    0.033333333333333 / [deg] Coordinate increment at reference point  
CUNIT1  = 'deg'                / Units of coordinate increment and value        
CUNIT2  = 'deg'                / Units of coordinate increment and value        
CTYPE1  = 'RA---CAR'           / Right ascension, plate caree projection        
CTYPE2  = 'DEC--CAR'           / Declination, plate caree projection            
CRVAL1  =                180.0 / [deg] Coordinate value at reference point      
CRVAL2  =                  0.0 / [deg] Coordinate value at reference point      
LONPOLE =                  0.0 / [deg] Native longitude of celestial pole       
LATPOLE =                 90.0 / [deg] Native latitude of celestial pole        
MJDREF  =                  0.0 / [d] MJD of fiducial time                       
RADESYS = 'ICRS'               / Equatorial coordinate system                   END
```

## Example usage

For a simple example that loads and interacts with the simulations, see the [example_usage.py](https://github.com/simonsobs/map_based_simulations/blob/master/mbs-s0015-20240504/example_usage.py) script.

### Additional simulations

If your analysis needs more simulations, it is possible to draw additional simulations from the provided noise models. This requires installing the [`mnms`](https://github.com/simonsobs/mnms) and [`sofind`](https://github.com/simonsobs/sofind) python libraries. Follow the "quick setup" described in the sofind readme.

An example of loading or simulating additional maps using `mnms` is provded in the [additional_simulations.py](https://github.com/simonsobs/map_based_simulations/blob/master/mbs-s0015-20240504/additional_simulations.py) script.

For an example of how to generate a larger set of simulations on a cluster, see the [run01](https://github.com/simonsobs/map_based_simulations/blob/master/mbs-s0015-20240504/runs/run01) script.
For reference, drawing the simulations provided here took approximately 5 hours using 20 MPI tasks distributed over 5 128-core nodes.

## Known issues

* Small scales (l > 4000) f030/f040 has excess noise power. Large scales (l < 1000) in f030/f040 has excess TT noise power. Large scales (l < 500) in f150 has excess TT noise power and large scales (l < 1000) in f290 has excess TT noise power. All relatively small amounts. See [these slides](https://drive.google.com/file/d/1ua8AmFIUonuAgn67LnM8IgIHIxONSawP/view?usp=sharing).

## Feedback

If anything looks suspicious in the simulations, please do not hesitate to [open an issue here](https://github.com/simonsobs/mnms/issues/new).
