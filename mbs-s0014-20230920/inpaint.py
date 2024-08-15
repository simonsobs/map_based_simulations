'''
Inpaint the corners of 2D Fourier space. This is unfortunately needed for the tiled 
and directional wav. models in mnms at the moment.
'''

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import os
import numpy as np

import healpy as hp
from pixell import enmap, sharp, curvedsky, reproject, enplot
from optweight import mat_utils, alm_c_utils

opj = os.path.join

mapdir = '/mnt/home/aduivenvoorden/project/so/20230524_sat_noise/v1'
cardir = '/mnt/home/aduivenvoorden/project/so/20230524_sat_noise/v1/car'
maskdir = opj(cardir, 'masks')
ratiodir = opj(cardir, 'ratios')
imgdir = opj(mapdir, 'img_car')
specdir = opj(mapdir, 'spec')

os.makedirs(imgdir, exist_ok=True)
os.makedirs(specdir, exist_ok=True)
os.makedirs(ratiodir, exist_ok=True)

freqs = ['f030', 'f040', 'f090', 'f150', 'f230', 'f290']
nsides = {'f030' : 128, 'f040' : 128, 'f090' : 512, 'f150' : 512, 'f230' : 1024, 'f290' : 1024}

ratios = np.load(opj(ratiodir, 'ratios.npy'))

freq_pairs = [('f030', 'f040'), ('f090', 'f150'), ('f230', 'f290')]


for paidx, pair in enumerate(freq_pairs):

    mask_obs = enmap.read_map(opj(maskdir, f'coadd_SAT_{pair[0]}_{pair[1]}_mask_obs.fits'))
    
    for fridx, freq in enumerate(pair):

        fidx = paidx * 2 + fridx
        
        for sidx in range(1, 3):

            imap = enmap.read_map(opj(cardir,  f'coadd_SAT_{freq}_2way_set0{sidx-1}_map.fits'))
            ivar = enmap.read_map(opj(cardir,  f'coadd_SAT_{freq}_2way_set0{sidx-1}_ivar.fits'))        

            imap = imap.astype(np.float64)
            ivar = ivar.astype(np.float64)

            imap *= mask_obs
            ivar *= mask_obs
            
            # Upgrade to I, Q, U.
            ivar = enmap.ones((3,) + ivar.shape[-2:], wcs=ivar.wcs) * ivar
            ivar[0] /= ratios[fidx,sidx-1,0]
            # Factor 2 is to compenstate for factor to in ratio.
            ivar[1:3] /= np.mean(ratios[fidx,sidx-1,1:3]) * 2

            # Draw noise.
            sqrt_var = mat_utils.matpow(ivar.reshape((3, np.prod(ivar.shape[-2:]))),
                                        -0.5, return_diag=True)
            noise = np.random.randn(*ivar.shape) * sqrt_var.reshape(ivar.shape)

            npol = noise.shape[0]
            font_size = 40 if freq in ('f030', 'f040') else 120

            # Create low-pass filter.
            lmax_low = int(2.5 * nsides[freq])
            lmax_large = int(np.round(180/np.abs(imap.wcs.wcs.cdelt[1])))
            ainfo = sharp.alm_info(lmax_large)            
            lwidth = max(50, int(lmax_low * 0.05))
            lowpass_filt = np.ones(lmax_large + 1)
            lowpass_filt[lmax_low-lwidth:lmax_low+1] *= hp.gauss_beam(2 * np.pi / lwidth, lmax=lwidth)
            lowpass_filt[lmax_low:] = 0
                            
            # Now only add noise beyond bandlimit to imap.
            # This trick uses that f**2 + (1 - (1 - sqrt(1 - f**2)))**2 = 1.
            # This is how orphics implements this.
            lowpass = noise.copy()
            alm = curvedsky.map2alm(noise, ainfo=ainfo, spin=[0, 2])            
            alm_c_utils.lmul(alm, 1 - np.sqrt(1 - lowpass_filt ** 2), ainfo, inplace=True)
            curvedsky.alm2map(alm, lowpass, ainfo=ainfo, spin=[0, 2])
            noise -= lowpass

            fig, ax = plt.subplots(dpi=300)
            ax.plot(lowpass_filt)
            fig.savefig(opj(imgdir, f'coadd_SAT_{freq}_00{sidx}of002_filters'))
            plt.close()
            
            alm = curvedsky.map2alm(imap, ainfo=ainfo, spin=[0, 2])
            alm_c_utils.lmul(alm, lowpass_filt, ainfo, inplace=True)
            imap_lowpass = curvedsky.alm2map(alm, imap, ainfo=ainfo, spin=[0, 2])
                
            imap = imap_lowpass + noise

            # Get mask.
            mask = (ivar[0].astype(bool)).astype(ivar.dtype)
            mask = enmap.apod_mask(mask, width=np.radians(5), edge=False)
            mask[mask < 0.7] = 0
            mask[mask >= 0.7] = 1
            # Apodize again.
            mask = enmap.apod_mask(mask, width=np.radians(5), edge=False)        
            mask_eff = ivar[0] / ivar[0].max() * mask

            ells = np.arange(lmax_large + 1)
            alm = curvedsky.map2alm(imap * mask_eff, ainfo=ainfo)
            nl = ainfo.alm2cl(alm[:,None,:], alm[None,:,:])

            alm_lowpass = curvedsky.map2alm(imap_lowpass * mask_eff, ainfo=ainfo)
            nl_lowpass = ainfo.alm2cl(alm_lowpass[:,None,:], alm_lowpass[None,:,:])
            
            alm_noise = curvedsky.map2alm(noise * mask_eff, ainfo=ainfo)
            nl_noise = ainfo.alm2cl(alm_noise[:,None,:], alm_noise[None,:,:])

            # Make a plot as a sanity check.
            fig, axs = plt.subplots(ncols=3, nrows=3, dpi=300, constrained_layout=True)
            for aidxs, ax in np.ndenumerate(axs):                
                axs[aidxs].plot(ells, nl[aidxs[0],aidxs[1]],
                                lw=0.5)
                axs[aidxs].plot(ells, nl_noise[aidxs[0],aidxs[1]],
                                lw=0.5)
                axs[aidxs].plot(ells, nl_lowpass[aidxs[0],aidxs[1]],
                                lw=0.5)
                
                if aidxs[0] == aidxs[1]:
                    axs[aidxs].set_yscale('log')
                    
            fig.savefig(opj(imgdir, f'coadd_SAT_{freq}_00{sidx}of002_spectra_inpaint'))            
            plt.close(fig)

            mapname2write = f'coadd_SAT_{freq}_2way_set{sidx-1:02d}_map_inpaint'
            enmap.write_fits(opj(cardir, f'{mapname2write}.fits'), imap.astype(np.float32))

            # Add symlink for ivar maps.
            os.remove(opj(cardir,  f'coadd_SAT_{freq}_2way_set0{sidx-1}_ivar_inpaint.fits'))
            os.symlink(opj(cardir,  f'coadd_SAT_{freq}_2way_set0{sidx-1}_ivar.fits'),
                       opj(cardir,  f'coadd_SAT_{freq}_2way_set0{sidx-1}_ivar_inpaint.fits'))


