'''
Construct an apodized mask used for power spectrum estimation.
'''
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import os
import numpy as np

from pixell import enmap, enplot

opj = os.path.join

mapdir = '/mnt/home/aduivenvoorden/project/so/20230524_sat_noise/v1'
cardir = opj(mapdir, 'car')
maskdir = opj(cardir, 'masks')
imgdir = opj(mapdir, 'img_car')

os.makedirs(imgdir, exist_ok=True)
os.makedirs(maskdir, exist_ok=True)

freq_pairs = [('f030', 'f040'), ('f090', 'f150'), ('f230', 'f290')]

for pair in freq_pairs:

    mask_obs = enmap.read_map(opj(maskdir, f'coadd_SAT_{pair[0]}_{pair[1]}_mask_obs.fits'))
    mask_obs = mask_obs.astype(bool)
    
    mask_est = enmap.shrink_mask(mask_obs, np.radians(5))
    mask_est = mask_est.astype(np.float32)
    mask_est = enmap.apod_mask(mask_est, width=np.radians(5), edge=False)

    plot = enplot.plot(mask_est, ticks=30, colorbar=True)
    enplot.write(opj(imgdir, f'coadd_SAT_{pair[0]}_{pair[1]}_mask_est'), plot)
                       
    enmap.write_map(opj(maskdir, f'coadd_SAT_{pair[0]}_{pair[1]}_mask_est.fits'), mask_est)
