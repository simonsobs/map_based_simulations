import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import median_abs_deviation
from mpi4py import MPI
from pixell import enmap, enplot

comm = MPI.COMM_WORLD
opj = os.path.join

# NOTE, these are paths on the CCA rusty cluster.
idir = '/mnt/home/aduivenvoorden/project/so/20240504_mss0002/RC1.r01'
odir = '/mnt/home/aduivenvoorden/project/so/20240504_mss0002_lat/masks'

# Paths on NERSC would be:
# idir = '/global/cfs/cdirs/sobs/sims/mss-0002/RC1.r01'
# odir = '/global/cfs/cdirs/sobs/v4_sims/mbs/mbs_s0015_20240504/masks'

imgdir = opj(odir, 'img')

if comm.rank == 0:
    os.makedirs(imgdir, exist_ok=True)

freqs = [('f030', 'f040'), ('f090', 'f150'), ('f230', 'f290')]
splits = ['split0', 'split1', 'split2', 'split3']

for freq_pair in freqs[comm.rank::comm.size]:

    shape, wcs = enmap.read_map_geometry(
        opj(idir, f'sobs_RC1.r01_LAT_mission_{freq_pair[0]}_4way_split0_sky_ivar_car.fits'))

    mask_obs = enmap.ones(shape, wcs=wcs, dtype=bool)

    for freq in freq_pair:

        fig, ax = plt.subplots(dpi=300)

        for sidx, split in enumerate(splits):
            ivarname = f'sobs_RC1.r01_LAT_mission_{freq}_4way_{split}_sky_ivar_car'
            ivar = enmap.read_map(opj(idir, f'{ivarname}.fits'))

            ivar_nonzero = ivar[ivar != 0]
            median = np.median(ivar_nonzero)

            lower_cut = 1e-3 * median

            ax.hist(np.log10(ivar[ivar != 0]), bins=1000, color=f'C{sidx}',
                    histtype='step')

            ax.axvline(np.log10(lower_cut), color=f'C{sidx}')

            mask_obs *= ivar >= lower_cut
                
        ax.set_xlabel('log ivar')
        ax.set_yscale('log')
        fig.savefig(opj(imgdir, f'hist_{freq}'))
        plt.close(fig)

    plot = enplot.plot(mask_obs, downgrade=4, colorbar=True, ticks=30)
    enplot.write(opj(imgdir, f'LAT_{freq_pair[0]}_{freq_pair[1]}_mask_obs'), plot)

    if freq_pair == ('f030', 'f040'):
        
        mask_obs = enmap.upgrade(mask_obs, 2)
    
    # Save mask obs
    enmap.write_map(opj(odir, f'LAT_{freq_pair[0]}_{freq_pair[1]}_mask_obs.fits'),
                    mask_obs.astype(np.float32))
    
    # Create mask est
    mask_est = enmap.shrink_mask(mask_obs, np.radians(1))
    mask_est = enmap.apod_mask(mask_est.astype(np.float32), width=np.radians(1))

    enmap.write_map(opj(odir, f'LAT_{freq_pair[0]}_{freq_pair[1]}_mask_est.fits'),
                    mask_est)
    
    plot = enplot.plot(mask_est, downgrade=4, colorbar=True, ticks=30)
    enplot.write(opj(imgdir, f'LAT_{freq_pair[0]}_{freq_pair[1]}_mask_est'), plot)    
