'''
Compare the power spectra of one of the sim to the data.
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
simdir = '/mnt/home/aduivenvoorden/project/actpol/maps/mnms/sims'
maskdir = opj(cardir, 'masks')
ratiodir = opj(cardir, 'ratios')
imgdir = opj(mapdir, 'img_car')
specdir = opj(mapdir, 'spec')

os.makedirs(imgdir, exist_ok=True)
os.makedirs(specdir, exist_ok=True)
os.makedirs(ratiodir, exist_ok=True)

freqs = ['f030', 'f040', 'f090', 'f150', 'f230', 'f290']
aposcale = 2.5

sidx = 1

freq_pairs = [('f030', 'f040'), ('f090', 'f150'), ('f230', 'f290')]
sim_idx = 1
#simtype = 'fdw'
simtype = 'tile'

simdict = {'f030' : [f'so_sat_v1_f1_{simtype}_lf_lf_f030_lf_f040_lmax405_2way_set{sidx-1}_noise_sim_map{sim_idx:04d}.fits',
                     np.s_[0,...]],
           'f040' : [f'so_sat_v1_f1_{simtype}_lf_lf_f030_lf_f040_lmax405_2way_set{sidx-1}_noise_sim_map{sim_idx:04d}.fits',
                     np.s_[1,...]],
           'f090' : [f'so_sat_v1_f1_{simtype}_mf_mf_f090_mf_f150_lmax1620_2way_set{sidx-1}_noise_sim_map{sim_idx:04d}.fits',
                     np.s_[0,...]],
           'f150' : [f'so_sat_v1_f1_{simtype}_mf_mf_f090_mf_f150_lmax1620_2way_set{sidx-1}_noise_sim_map{sim_idx:04d}.fits',
                     np.s_[1,...]],
           'f230' : [f'so_sat_v1_f1_{simtype}_uhf_uhf_f230_uhf_f290_lmax3240_2way_set{sidx-1}_noise_sim_map{sim_idx:04d}.fits',
                     np.s_[0,...]],
           'f290' : [f'so_sat_v1_f1_{simtype}_uhf_uhf_f230_uhf_f290_lmax3240_2way_set{sidx-1}_noise_sim_map{sim_idx:04d}.fits',
                     np.s_[1,...]]}
lmax_dict = {'f030' : 405, 'f040' : 405, 'f090' : 1620, 'f150' : 1620, 'f230' : 3240, 'f290' : 3240}

for pair in freq_pairs:

    mask = enmap.read_map(opj(maskdir, f'coadd_SAT_{pair[0]}_{pair[1]}_mask_est.fits'))

    for freq in pair:

        #for sidx in range(1, 3):
        for _ in [1]:
            
            imap = enmap.read_map(opj(cardir,  f'coadd_SAT_{freq}_2way_set0{sidx-1}_map_inpaint.fits'))
            ivar = enmap.read_map(opj(cardir,  f'coadd_SAT_{freq}_2way_set0{sidx-1}_ivar_inpaint.fits'))

            sim = enmap.read_map(opj(simdir, simdict[freq][0]), sel=simdict[freq][1])[0]
                                 
            for weight in ['flat', 'ivar']:

                mask_eff = enmap.zeros((1,) + ivar.shape[-2:], dtype=ivar.dtype, wcs=ivar.wcs)

                if weight == 'ivar':
                    mask_eff[0] = ivar[0] / ivar[0].max() * mask
                else:
                    mask_eff[0] = mask

                mask_eff_dg = enmap.project(mask_eff, sim.shape[-2:], sim.wcs)

                lmax = lmax_dict[freq]                
                ainfo = sharp.alm_info(lmax)
                ells = np.arange(lmax + 1)
                                 
                alm = curvedsky.map2alm(imap * mask_eff, ainfo=ainfo)
                nl = ainfo.alm2cl(alm[:,None,:], alm[None,:,:])

                alm_sim = curvedsky.map2alm(sim * mask_eff_dg, ainfo=ainfo)
                nl_sim = ainfo.alm2cl(alm_sim[:,None,:], alm_sim[None,:,:])
                
                fig, axs = plt.subplots(ncols=3, nrows=3, dpi=300, constrained_layout=True)

                for aidxs, ax in np.ndenumerate(axs):
                    
                    if aidxs[0] == aidxs[1]:
                    
                        axs[aidxs].plot(ells, nl[aidxs[0],aidxs[1]],
                                        lw=0.5)
                        axs[aidxs].plot(ells, nl_sim[aidxs[0],aidxs[1]],
                                        lw=0.5)
                    else:

                        num = nl[aidxs[0],aidxs[1]]
                        den = np.sqrt(nl[aidxs[0],aidxs[0]] *  nl[aidxs[1],aidxs[1]])                        
                        rho = np.zeros_like(num)
                        np.divide(num, den, where=den != 0, out=rho)

                        
                        axs[aidxs].plot(ells, rho, lw=0.5)

                        num = nl_sim[aidxs[0],aidxs[1]]
                        den = np.sqrt(nl_sim[aidxs[0],aidxs[0]] *  nl_sim[aidxs[1],aidxs[1]])                        
                        rho = np.zeros_like(num)
                        np.divide(num, den, where=den != 0, out=rho)
                        
                        axs[aidxs].plot(ells, rho, lw=0.5)
                                            
                    if aidxs[0] == aidxs[1]:
                        axs[aidxs].set_yscale('log')

                    axs[aidxs].set_xlim(1)
                    axs[aidxs].set_xscale('log')                    
                        
                fig.savefig(opj(imgdir, f'coadd_SAT_{freq}_00{sidx}of002_spectra_sim_compared_{weight}'))
                
                for aidxs, ax in np.ndenumerate(axs):

                    if aidxs[0] == aidxs[1]:
                        axs[aidxs].set_yscale('linear')
                    # This is a fun bug in matplotlib.
                    axs[aidxs].set_xscale('linear')
                    axs[aidxs].set_xscale('log')
                    axs[aidxs].set_xscale('linear')                    
                    axs[aidxs].set_xlim(0, 200)
                fig.savefig(opj(imgdir, f'coadd_SAT_{freq}_00{sidx}of002_spectra_sim_compared_{weight}_linear'))                
                plt.close(fig)

            # Also plot maps weighted by sqrt(ivar).
            mask_eff = enmap.zeros((1,) + ivar.shape[-2:], dtype=ivar.dtype, wcs=ivar.wcs)
            mask_eff[0] = ivar[0] * np.sqrt(ivar[0]) * mask

            lmax = lmax_dict[freq] * 2
            ainfo = sharp.alm_info(lmax)
            ells = np.arange(lmax + 1)

            alm = curvedsky.map2alm(imap * mask_eff, ainfo=ainfo)
            nl = ainfo.alm2cl(alm[:,None,:], alm[None,:,:])

            fig, axs = plt.subplots(ncols=3, nrows=3, dpi=300, constrained_layout=True)

            for aidxs, ax in np.ndenumerate(axs):

                axs[aidxs].plot(ells, nl[aidxs[0],aidxs[1]],
                                lw=0.5)
                
                if aidxs[0] == aidxs[1]:
                    axs[aidxs].set_yscale('log')

                axs[aidxs].set_xlim(1)
                axs[aidxs].set_xscale('log')                    

            fig.savefig(opj(imgdir, f'coadd_SAT_{freq}_00{sidx}of002_spectra_sqrt_ivar'))
            plt.close(fig)
