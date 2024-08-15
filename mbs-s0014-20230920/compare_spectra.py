'''
Check that noise spectra of reprojected maps from reproject.py agree with spectra from
the input healpix maps. This also computes a set of ratios between white noise from ivar
anad the actual noise power spectra which is used as an input to inpaint.py
'''
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import os
import numpy as np

import healpy as hp
import pymaster as nmt
from pixell import enmap, sharp, curvedsky, reproject
from optweight import mat_utils

opj = os.path.join

mapdir = '/mnt/home/aduivenvoorden/project/so/20230524_sat_noise/v1'
cardir = '/mnt/home/aduivenvoorden/project/so/20230524_sat_noise/v1/car'
ratiodir = opj(cardir, 'ratios')
imgdir = opj(mapdir, 'img_car')
specdir = opj(mapdir, 'spec')

os.makedirs(imgdir, exist_ok=True)
os.makedirs(specdir, exist_ok=True)
os.makedirs(ratiodir, exist_ok=True)

freqs = ['f030', 'f040', 'f090', 'f150', 'f230', 'f290']
aposcale = 2.5

ratios = np.ones((len(freqs), 2, 3)) # nfreq, nsplit, npol.

for fidx, freq in enumerate(freqs):

    for sidx in range(1, 3):

        imap = hp.read_map(
            opj(mapdir, f'coadd_SAT_{freq}_00{sidx}of002_map.fits'),
            field=None)
        imap[imap == hp.UNSEEN] = 0
        imap *= 1e6
        nside = hp.npix2nside(imap.shape[-1])
        lmax = int(2.5 * nside)
        ells = np.arange(lmax + 1)
        ainfo = sharp.alm_info(lmax)
        
        icov = hp.read_map(
            opj(mapdir, f'coadd_SAT_{freq}_00{sidx}of002_invcov.fits'),
            field=None)
        icov[icov == hp.UNSEEN] = 0
        icov *= 1e-12

        imap_car = enmap.read_map(opj(cardir,  f'coadd_SAT_{freq}_2way_set0{sidx-1}_map.fits'))
        ivar_car = enmap.read_map(opj(cardir,  f'coadd_SAT_{freq}_2way_set0{sidx-1}_ivar.fits'))        

        # Draw noise realization.
        sqrt_var = mat_utils.matpow(ivar_car.reshape(1, np.prod(ivar_car.shape[-2:])),
                                    -0.5, return_diag=True)
        noise_car = np.random.randn(*ivar_car.shape) * sqrt_var.reshape(ivar_car.shape)
        
        ivar = np.zeros((3, icov.shape[-1]), dtype=icov.dtype)
        ivar[0] = icov[0]
        ivar[1] = icov[3]
        ivar[2] = icov[5]

        mask = (ivar.astype(bool)).astype(ivar.dtype)

        # Shrink mask        
        mask[0] = nmt.mask_apodization(mask[0], 5, apotype="C1")
        mask[1] = nmt.mask_apodization(mask[1], 5, apotype="C1")
        mask[2] = nmt.mask_apodization(mask[2], 5, apotype="C1")
        mask[mask < 0.7] = 0
        mask[mask >= 0.7] = 1
        # Apodize again.
        mask[0] = nmt.mask_apodization(mask[0], aposcale, apotype="C1")
        mask[1] = nmt.mask_apodization(mask[1], aposcale, apotype="C1")
        mask[2] = nmt.mask_apodization(mask[2], aposcale, apotype="C1")
        
        for weight in ['flat', 'ivar']:

            mask_eff = np.zeros((3, ivar.shape[-1]), dtype=ivar.dtype)
            if weight == 'ivar':
                mask_eff[0] = ivar[0] / ivar[0].max() * mask[0]
                mask_eff[1] = ivar[1] / ivar[1].max() * mask[1]
                mask_eff[1] = ivar[2] / ivar[2].max() * mask[2]
            else:
                mask_eff[0] = mask[0]
                mask_eff[1] = mask[1]
                mask_eff[1] = mask[2]

            # Extensive is False here because we only use ivar as a pixel mask.
            extensive = False
            mask_eff_car = reproject.healpix2map(mask_eff, shape=imap_car.shape, wcs=imap_car.wcs,
                                                 extensive=extensive, method='spline', order=1, spin=0)

            alm = hp.map2alm(imap * mask_eff, lmax)
            nl = ainfo.alm2cl(alm[:,None,:], alm[None,:,:])

            alm_car = curvedsky.map2alm(imap_car * mask_eff_car, ainfo=ainfo)
            nl_car = ainfo.alm2cl(alm_car[:,None,:], alm_car[None,:,:])

            alm_noise = curvedsky.map2alm(noise_car * mask_eff_car[0], ainfo=ainfo)
            nl_noise = ainfo.alm2cl(alm_noise[:,None,:], alm_noise[None,:,:])

            # Determine ratio of the noise power in the maps over draw from ivar.
            ell_low = int(0.9 * lmax)
            ell_high = int(0.95 * lmax)

            if weight == 'ivar':
                ratios[fidx,sidx-1,0] = np.mean(nl_car[0,0,ell_low:ell_high]) / \
                    np.mean(nl_noise[0,0,ell_low:ell_high])
                ratios[fidx,sidx-1,1] = np.mean(nl_car[1,1,ell_low:ell_high]) / \
                    np.mean(nl_noise[0,0,ell_low:ell_high])
                ratios[fidx,sidx-1,2] = np.mean(nl_car[2,2,ell_low:ell_high]) / \
                    np.mean(nl_noise[0,0,ell_low:ell_high])
            
            fig, axs = plt.subplots(ncols=3, nrows=3, dpi=300, constrained_layout=True)
            
            for aidxs, ax in np.ndenumerate(axs):                
                axs[aidxs].plot(ells, nl[aidxs[0],aidxs[1]],
                                lw=0.5)
                axs[aidxs].plot(ells, nl_car[aidxs[0],aidxs[1]],
                                lw=0.5)
                if aidxs[0] == aidxs[1]:
                    fact = 2 if aidxs[0] > 0 else 1
                    axs[aidxs].plot(ells, nl_noise[0,0] * fact,
                                    lw=0.5)
                    
                if aidxs[0] == aidxs[1]:
                    axs[aidxs].set_yscale('log')
                
            fig.savefig(opj(imgdir, f'coadd_SAT_{freq}_00{sidx}of002_spectra_compared_{weight}'))            
            plt.close(fig)

np.save(opj(ratiodir, 'ratios.npy'), ratios)
print(ratios)
