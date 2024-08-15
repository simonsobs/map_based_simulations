from packaging.version import Version
import numpy as np
import pixell
from pixell import enmap, curvedsky, enplot
from os.path import join

assert Version(pixell.__version__) >= Version('0.19'), "We require pixell version > 0.19 (change from libsharp to ducc)"

# Note, this script it set up to be run on NERSC.

# first get some basic info like the path and the filename template
fdir = '/global/cfs/cdirs/sobs/v4_sims/mbs/mbs_s0015_20240504/sims'
fbase_template = 'so_lat_mbs_mss0002_{model}_{bands}_lmax5400_4way_set{split_num}_noise_sim_map{sim_num:04}.fits'

# For models, pick from 'fdw_lf', 'fdw_mf' or 'fdw_uhf'. The corresponding entries for
# the bands are: 'lf_f030_lf_f040', 'mf_f090_mf_f150' and uhf_f230_uhf_f290.

# Let's load the sim for e.g. f150, split 2, sim 123
model = 'fdw_mf'
bands = 'mf_f090_mf_f150'
band_idx = 1                # f090 is 0, f150 is 1
split_num = 2
sim_num = 123               # has 4 digits (leading 0's), but padding done for us in template

sim = enmap.read_map(
    join(fdir, fbase_template.format(
        model=model,
        bands=bands,
        split_num=split_num,
        sim_num=sim_num)
        ),
    sel=np.s_[band_idx, 0]  # just load f150, remove split axis
    )
print(sim.geometry, sim.dtype)

assert sim.shape == (3, 2640, 10800)
assert np.allclose(sim.wcs.wcs.cdelt, [-0.03333333, 0.03333333])
assert np.allclose(sim.wcs.wcs.crval, [180, 0])
assert np.allclose(sim.wcs.wcs.crpix, [5400.62, 1890.50])
assert sim.dtype == np.float32

# The sim only contains noise power to the Nyquist frequency of the pixelization (for 2 arcmin pixels, `lmax=5400`).
# But what if we wanted to work with objects in map-space defined at the full resolution of the data, for example a
# sky mask defined at 0.5 arcmin resolution? We need to project the `sim` to our desired geometry.

# Because the `sim` is bandlimited, we can do this losslessly with a spherical harmonic transform:

# First we need the geometry of the pixelization.
# We can get this from one of the time-domain simulations
shape, wcs = enmap.read_map_geometry(
    '/global/cfs/cdirs/sobs/sims/mss-0002/RC1.r01/sobs_RC1.r01_LAT_mission_f150_4way_split1_noise_map_car.fits')

# Allocate an empty map to hold the sim at full resolution
sim_fullres = enmap.empty((*sim.shape[:-2], *shape[-2:]), wcs, sim.dtype)

# Project sim to alm, then from alm to map

# High res vesion:
#curvedsky.alm2map(curvedsky.map2alm(sim, lmax=5400), sim_fullres)

# Low res version for quick testing:
curvedsky.alm2map(curvedsky.map2alm(sim, lmax=300), sim_fullres)

# Finally, we can save plots of the I, Q and U components of the simulated map as png files.
# Note that if you are working in an interactive notebook, you can replace the
# "enplot.plot" and "enplot.write" calls with "enplot.pshow" to just show the plots.
for pidx, pol in enumerate(['I', 'Q', 'U']):
    plot = enplot.plot(sim_fullres[pidx], downgrade=32, colorbar=True, ticks=15)
    enplot.write(f'example_plot_{pol}', plot)
