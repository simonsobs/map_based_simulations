import os

import numpy as np
from mpi4py import MPI
from pixell import enmap, enplot

comm = MPI.COMM_WORLD
opj = os.path.join

idir = '/mnt/home/aduivenvoorden/project/so/20240504_mss0002/RC1.r01'
imgdir = '/mnt/home/aduivenvoorden/project/so/20240504_mss0002_lat/input/img'

if comm.rank == 0:
    os.makedirs(imgdir, exist_ok=True)

freqs = ['f030', 'f040', 'f090', 'f150', 'f230', 'f290']
splits = ['coadd', 'split0', 'split1', 'split2', 'split3']

freqs_splits = []

for freq in freqs:    
    for split in splits:
        freqs_splits.append((freq, split))

for freq, split in freqs_splits[comm.rank::comm.size]:

    mapname = f'sobs_RC1.r01_LAT_mission_{freq}_4way_{split}_noise_map_car'
    imap = enmap.read_map(opj(idir, f'{mapname}.fits'))

    plot = enplot.plot(imap[0], downgrade=8, font_size=50, ticks=30, colorbar=True)
    enplot.write(opj(imgdir, f'{mapname}_0'), plot)    
    for pidx in range(1, 3):
        plot = enplot.plot(imap[pidx], downgrade=8, font_size=50, ticks=30, colorbar=True)
        enplot.write(opj(imgdir, f'{mapname}_{pidx}'), plot)

    del imap
    
    ivarname = f'sobs_RC1.r01_LAT_mission_{freq}_4way_{split}_sky_ivar_car'
    ivar = enmap.read_map(opj(idir, f'{ivarname}.fits'))

    plot = enplot.plot(ivar, downgrade=8, font_size=50, ticks=30, colorbar=True)
    enplot.write(opj(imgdir, ivarname), plot)
    
