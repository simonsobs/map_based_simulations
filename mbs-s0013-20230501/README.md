# Map-based noise simulations based on the LAT `scan-s0003` time-domain simulations

Tag: `mbs-s0013-20230501`

## Updates

* 2023-05-09: first release, `lmax=5400` simulations.

## Summary

300 realistic realizations of the LAT map noise, given the single realization of the time-domain simulations. Simulations cover the full LAT footprint to a bandlimit of `lmax=5400`, and utilize the directional wavelet noise model.

## Noise model

This release is based on the LAT `scan-s0003` time-domain simulations, available on `NERSC` at:

    /global/cfs/cdirs/sobs/sims/scan-s0003/output/combined/processed/fejer1

These time-domain simulations implement the type-1.2.1 high-cadence 3-elevation scan-strategy (see scan-strategy [repo](https://github.com/simonsobs/pwg-scripts/tree/master/pwg-tds/scan-strategy-sims-2023) and [ICD](https://docs.google.com/presentation/d/1hInPLZYGQrO1E7j9FxR6UlH5RZarJsQ3mDHzlU0i7I8/edit#slide=id.p)). These maps provide a single realization of the noise in each split of each frequency band. More information is also available on the SO [productdb](https://www.productdb.simonsobservatory.org/product/simulation/scan-s0003) and [confluence](https://simonsobs.atlassian.net/wiki/spaces/PRO/pages/96862289/scan-s0003+-+Scanning+strategy+simulations).

Using [`mnms`](https://github.com/simonsobs/mnms) (commit `d4afb9d`), we generate 300 realizations of the noise using map-based methods. Specifically, we use the directional wavelet model, governed by the configured [parameters](parameters/so_scan_s0003.yaml).

Notes:
* Simulations are bandlimited to `lmax=5400`. To save space, the simulations are stored in a pixelization that is downgraded by a factor of 4 relative to the time-domain simulations (`shape=(..., 2640, 10800)`, 2 arcmin resolution vs. `shape=(..., 10560, 43200)` 0.5 arcmin resolution). See [examples](#example-usage) below for further guidance.
* The time-domain simulations are produced in the Clenshaw-Curtis CAR variant. The map-based simulations are first built using these Clenshaw-Curtis time-domain maps as inputs. Then, their `wcs` is adjusted *post-hoc* (by <1 pixel) to match what they would have been had the time-domain simulations been produced in the Fejer1 CAR variant as specified (see [this issue](https://github.com/simonsobs/map_based_simulations/issues/42) for more detail). We note this for the record; it does not impact users.

## Available maps

Maps are available in the CAR (Fejer1 variant) pixelization. As above, the maps have a resolution of 2 arcmin. Maps are in Equatorial Coordinates, `uK_CMB` units, FITS format.

The maps are located here:

    /global/cfs/cdirs/sobs/v4_sims/mbs/mbs-s0013-20230501/sims

and have the following naming convention:

    so_scan_s0003_fdw_{bands}_lmax5400_4way_set{split_num}_noise_sim_map{sim_num:04}.fits

where `bands` is in `[lf_f030_lf_f040, mf_f090_mf_f150, uhf_f230_uhf_f290]`, `split_num` is in `[0-3]` and `sim_num` is in `[0000-0299]`.

Please [open an issue here](https://github.com/simonsobs/map_based_simulations/issues/new) for any data access problems.

## Available models

The covariance matrices from which simulations are drawn are available here: 

    /global/cfs/cdirs/sobs/v4_sims/mbs/mbs-s0013-20230501/models

Due to issues with the Clenshaw-Curtis vs. Fejer1 geometry, they do not currently support drawing additional realizations.

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
CRPIX1  =             5400.625 / Pixel coordinate of reference point            
CRPIX2  =               1890.5 / Pixel coordinate of reference point            
CDELT1  =   -0.033333333333333 / [deg] Coordinate increment at reference point  
CDELT2  =    0.033333333333333 / [deg] Coordinate increment at reference point  
CUNIT1  = 'deg'                / Units of coordinate increment and value        
CUNIT2  = 'deg'                / Units of coordinate increment and value        
CTYPE1  = 'RA---CAR'           / Right ascension, plate caree projection        
CTYPE2  = 'DEC--CAR'           / Declination, plate caree projection            
CRVAL1  =                  0.0 / [deg] Coordinate value at reference point      
CRVAL2  =                  0.0 / [deg] Coordinate value at reference point      
LONPOLE =                  0.0 / [deg] Native longitude of celestial pole       
LATPOLE =                 90.0 / [deg] Native latitude of celestial pole        
MJDREF  =                  0.0 / [d] MJD of fiducial time                       
RADESYS = 'ICRS'               / Equatorial coordinate system                   END
```

## Example usage

We give some minimum working examples:
```python
import numpy as np
from pixell import enmap, curvedsky, enplot
from os.path import join

# first get some basic info like the path and the filename template
fdir = '/global/cfs/cdirs/sobs/v4_sims/mbs/mbs-s0013-20230501/sims'
fbase_template = 'so_scan_s0003_fdw_{bands}_lmax5400_4way_set{split_num}_noise_sim_map{sim_num:04}.fits'

# let's load the sim for e.g. f150, split 2, sim 123
bands = 'mf_f090_mf_f150'
band_idx = 1                # f090 is 0, f150 is 1
split_num = 2
sim_num = 123               # has 4 digits (leading 0's), but padding done for us in template

sim = enmap.read_map(
    join(fdir, fbase_template.format(
        bands=bands,
        split_num=split_num,
        sim_num=sim_num)
        ),
    sel=np.s_[band_idx, 0]  # just load f150, remove split axis
    )
print(sim.geometry, sim.dtype)
```
This should give:
```python
((3, 2640, 10800), car:{cdelt:[-0.03333,0.03333],crval:[0,0],crpix:[5400.62,1890.50]}) float32
```
As discussed, the `sim` only contains noise power to the Nyquist frequency of the pixelization (for 2 arcmin pixels, `lmax=5400`). But what if we wanted to work with objects in map-space defined at the full resolution of the data, for example a sky mask defined at 0.5 arcmin resolution? We need to project the `sim` to our desired geometry.

Because the `sim` is bandlimited, we can do this losslessly with a spherical harmonic transforms:
```python
# first we need the geometry of the pixelization.
# we can get this from one of the time-domain simulations
shape, wcs = enmap.read_map_geometry('/global/cfs/cdirs/sobs/sims/scan-s0003/output/combined/processed/fejer1/lat01_s25_fullfp_f150_1pass_4way_set02_map.fits')

# allocate an empty map to hold the sim at full resolution
sim_fullres = enmap.empty((*sim.shape[:-2], *shape[-2:]), wcs, sim.dtype)

# project sim to alm, then from alm to map
curvedsky.alm2map(curvedsky.map2alm(sim, lmax=5400), sim_fullres)
```
Finally, we can plot the sim:
```python
# can also plot all three components in one call, but the colorbar will
# be shared for all three plots. this is visually nicer for components
# with very different dynamic range, as in this case
for pol in range(3):
    enplot.pshow(sim_fullres[pol], downgrade=32, colorbar=True, ticks=15)
```

## Known issues

* Large-scale TT (l < 300) has excess noise power of > 10% in `f030-f090`, see [these slides](https://drive.google.com/drive/folders/1-VHHW8YbRubNix0qza3MfPqHRVey0eAX).

## Feedback

If anything looks suspicious in the simulations, please do not hesitate to [open an issue here](https://github.com/simonsobs/mnms/issues/new).
