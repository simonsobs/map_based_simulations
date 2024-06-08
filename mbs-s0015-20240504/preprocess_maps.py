'''
Rename the maps and additionally, resample the LF maps to 2x the resolution.
This is needed for mnms. 
'''

import os

import numpy as np
from pixell import enmap, enplot
from mnms import utils

opj = os.path.join

idir = '/mnt/home/aduivenvoorden/project/so/20240504_mss0002/RC1.r01'
odir = '/mnt/home/aduivenvoorden/project/so/20240504_mss0002_lat/renamed'
os.makedirs(odir, exist_ok=True)

freqs = ['f030', 'f040', 'f090', 'f150', 'f230', 'f290']
splits = ['split0', 'split1', 'split2', 'split3']

freqs_splits = []

for freq in freqs:    
    for split in splits:
        freqs_splits.append((freq, split))

for freq, split in freqs_splits:

    mapname_in = f'sobs_RC1.r01_LAT_mission_{freq}_4way_{split}_noise_map_car.fits'
    mapname_out = f'sobs_RC1.r01_LAT_mission_{freq}_4way_{split}_noise_map_car.fits'    
    
    ivarname_in = f'sobs_RC1.r01_LAT_mission_{freq}_4way_{split}_sky_ivar_car.fits'
    ivarname_out = f'sobs_RC1.r01_LAT_mission_{freq}_4way_{split}_noise_ivar_car.fits'    

    if freq in ['f030', 'f040']:
        
        shape, wcs = enmap.read_map_geometry(opj(idir, mapname_in))

        assert utils.get_variant(shape, wcs, atol=1e-6) == 'fejer1'
        
        shape_ug, wcs_ug = enmap.upgrade_geometry(shape, wcs, 2)
        imap = enmap.read_map(opj(idir, mapname_in))
        omap = utils.fourier_resample(imap, shape=(shape[0],) + shape_ug[-2:], wcs=wcs_ug)
        enmap.write_map(opj(odir, mapname_out), omap)
        del omap, imap

        ivar = enmap.read_map(opj(idir, ivarname_in))
        ivar = enmap.upgrade(ivar, 2) / 4 # Correction for change in pixel size.
        enmap.write_map(opj(odir, ivarname_out), ivar)        
        
    else:
        try:
            os.symlink(opj(idir, mapname_in), opj(odir, mapname_out))
        except FileExistsError as e:
            os.remove(opj(odir, mapname_out))
            os.symlink(opj(idir, mapname_in), opj(odir, mapname_out))

        try:            
            os.symlink(opj(idir, ivarname_in), opj(odir, ivarname_out))
        except FileExistsError as e:
            os.remove(opj(odir, ivarname_out))
            os.symlink(opj(idir, ivarname_in), opj(odir, ivarname_out))
