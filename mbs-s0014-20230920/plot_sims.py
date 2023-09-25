'''
Plot additional comparison between data and sims. Maps, 2D power spectra.
'''
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import os
import numpy as np
from scipy import ndimage
from scipy.interpolate import interp1d

from pixell import enmap, enplot, curvedsky, sharp
from optweight import alm_c_utils

opj = os.path.join

mapdir = '/mnt/home/aduivenvoorden/project/so/20230524_sat_noise/v1'
cardir = '/mnt/home/aduivenvoorden/project/so/20230524_sat_noise/v1/car'
simdir = '/mnt/home/aduivenvoorden/project/actpol/maps/mnms/sims'
maskdir = opj(cardir, 'masks')
ratiodir = opj(cardir, 'ratios')
imgdir = opj(mapdir, 'img_car/sims_compared')
specdir = opj(mapdir, 'spec')

os.makedirs(imgdir, exist_ok=True)
os.makedirs(specdir, exist_ok=True)
os.makedirs(ratiodir, exist_ok=True)

freqs = ['f030', 'f040', 'f090', 'f150', 'f230', 'f290']
aposcale = 2.5

#for fidx, freq in enumerate(freqs):

freq_pairs = [('f030', 'f040'), ('f090', 'f150'), ('f230', 'f290')]

sidx = 1
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

    mask = enmap.read_map(opj(maskdir, f'coadd_SAT_{pair[0]}_{pair[1]}_mask_obs.fits'))

    for freq in pair:

        font_size = 10 if freq in ('f030', 'f040') else 30
        lmax = lmax_dict[freq]
        
        #for sidx in range(1, 3):
        for sidx in [1]:

            imap = enmap.read_map(opj(cardir,  f'coadd_SAT_{freq}_2way_set0{sidx-1}_map_inpaint.fits'))
            ivar = enmap.read_map(opj(cardir,  f'coadd_SAT_{freq}_2way_set0{sidx-1}_ivar_inpaint.fits'))

            plot = enplot.plot(ivar, colorbar=True, ticks=30,
                               font_size=font_size)
            enplot.write(opj(imgdir, f'coadd_SAT_{freq}_2way_set0{sidx-1}_ivar_inpaint'), plot)

            mask_eff = mask

            #imap *= mask_eff
            #imap = imap.downgrade(2)

            sim = enmap.read_map(opj(simdir, simdict[freq][0]), sel=simdict[freq][1])[0]
            mask_dg = enmap.project(mask_eff, sim.shape[-2:], sim.wcs)
            ivar_dg = enmap.project(ivar, sim.shape[-2:], sim.wcs)
            ivar_dg[ivar_dg < 0] = 0
            sim *= mask_dg

            # Bandlimit TOD sim.
            alm = curvedsky.map2alm(imap, lmax=lmax_dict[freq])
            imap = curvedsky.alm2map(alm, sim * 0)

            imap *= mask_dg
            
            npol = imap.shape[0]
            tmin, tmax = (np.quantile(imap[0], 0.03), np.quantile(imap[0], 0.97))
            pmin, pmax = (np.quantile(imap[1], 0.03), np.quantile(imap[1], 0.97))
            vmin = [tmin, pmin, pmin]
            vmax = [tmax, pmax, pmax]

            for pidx in range(npol):
                plot = enplot.plot(imap[pidx], colorbar=True, ticks=30, min=vmin[pidx], max=vmax[pidx],
                                   font_size=font_size)
                enplot.write(opj(imgdir, f'coadd_SAT_{freq}_2way_set0{sidx-1}_map_inpaint_{pidx}'), plot)

                plot = enplot.plot(sim[pidx], colorbar=True, ticks=30, min=vmin[pidx], max=vmax[pidx],
                                   font_size=font_size)
                enplot.write(
                    opj(imgdir, f'coadd_SAT_{freq}_2way_set0{sidx-1}_map_inpaint_sim_{pidx}'), plot)

            # Plot scale-dependent variance.
            low_ell_filt_low = 20
            low_ell_filt_high = 100
            low_ell_filt = np.ones(lmax_dict[freq] + 1)
            low_ell_filt[:low_ell_filt_low] = 0
            low_ell_filt[low_ell_filt_high:] = 0

            high_ell_filt_low = 200
            high_ell_filt_high = 300
            high_ell_filt = np.ones_like(low_ell_filt)
            high_ell_filt[:high_ell_filt_low] = 0
            high_ell_filt[high_ell_filt_high:] = 0

            ainfo = sharp.alm_info(lmax)
            alm = curvedsky.map2alm(imap * np.sqrt(ivar_dg), lmax=lmax_dict[freq])
            alm = alm_c_utils.lmul(alm, low_ell_filt, ainfo)
            omap = curvedsky.alm2map(alm, imap * 0)
            omap = enmap.smooth_gauss(omap ** 2, np.radians(1))
            
            for pidx in range(3):
                plot = enplot.plot(omap[pidx], colorbar=True, ticks=30,
                                   font_size=font_size)
                enplot.write(opj(imgdir, f'coadd_SAT_{freq}_2way_set0{sidx-1}_var_est_low_{pidx}'), plot)

            alm = curvedsky.map2alm(imap * np.sqrt(ivar_dg), lmax=lmax_dict[freq])
            alm = alm_c_utils.lmul(alm, high_ell_filt, ainfo)
            omap = curvedsky.alm2map(alm, imap * 0)
            omap = enmap.smooth_gauss(omap ** 2, np.radians(1))

            for pidx in range(3):
                plot = enplot.plot(omap[pidx], colorbar=True, ticks=30,
                                   font_size=font_size)
                enplot.write(opj(imgdir, f'coadd_SAT_{freq}_2way_set0{sidx-1}_var_est_high_{pidx}'), plot)            

            alm = curvedsky.map2alm(sim * np.sqrt(ivar_dg), lmax=lmax_dict[freq])
            alm = alm_c_utils.lmul(alm, low_ell_filt, ainfo)
            omap = curvedsky.alm2map(alm, imap * 0)
            omap = enmap.smooth_gauss(omap ** 2, np.radians(1))
            
            for pidx in range(3):
                plot = enplot.plot(omap[pidx], colorbar=True, ticks=30,
                                   font_size=font_size)
                enplot.write(opj(imgdir, f'coadd_SAT_{freq}_2way_set0{sidx-1}_var_est_low_sim_{pidx}'), plot)

            alm = curvedsky.map2alm(sim * np.sqrt(ivar_dg), lmax=lmax_dict[freq])
            alm = alm_c_utils.lmul(alm, high_ell_filt, ainfo)
            omap = curvedsky.alm2map(alm, imap * 0)
            omap = enmap.smooth_gauss(omap ** 2, np.radians(1))

            for pidx in range(3):
                plot = enplot.plot(omap[pidx], colorbar=True, ticks=30,
                                   font_size=font_size)
                enplot.write(opj(imgdir, f'coadd_SAT_{freq}_2way_set0{sidx-1}_var_est_high_sim_{pidx}'), plot)            

                
            # Also plot 2D spectra.
            patches = [np.radians([[-55, 65], [-25, 95]]), np.radians([[5, 135], [-25, 165]])]
            for paidx, patch in enumerate(patches):

                # Extract patch.
                submap = enmap.submap(imap, patch)
                submap = enmap.apod(submap, int(lmax * 0.02))

                submap_sim = enmap.submap(sim, patch)
                submap_sim = enmap.apod(submap_sim, int(lmax * 0.02))

                if freq in ('f030', 'f040'):
                    upgrade = 4
                elif freq in ('f090', 'f150'):
                    upgrade = 2
                else:
                    upgrade = 1
                
                for pidx in range(npol):
                    plot = enplot.plot(
                        submap[pidx], colorbar=True, ticks=5, min=vmin[pidx], max=vmax[pidx],
                        upgrade=upgrade)
                    enplot.write(
                        opj(imgdir, f'coadd_SAT_{freq}_2way_set0{sidx-1}_submap_{paidx}_{pidx}'), plot)

                    plot = enplot.plot(
                        submap_sim[pidx], colorbar=True, ticks=5, min=vmin[pidx], max=vmax[pidx],
                        upgrade=upgrade)
                    enplot.write(
                        opj(imgdir, f'coadd_SAT_{freq}_2way_set0{sidx-1}_submap_sim_{paidx}_{pidx}'),
                        plot)

                fmap = enmap.map2harm(submap)
                fmap_sim = enmap.map2harm(submap_sim)
                lmap = fmap.modlmap()

                color = "1:000000,0:ffffff"

                nl2d = enmap.calc_ps2d(fmap[:,None,:,:], fmap[None,:,:,:])

                # Normalize to white noise floor.
                mean_0 = np.mean(nl2d[0,0,(lmap>int(0.7*lmax)) & (lmap<int(lmax))])
                mean_1 = np.mean(nl2d[1,1,(lmap>int(0.7*lmax)) & (lmap<int(lmax))])
                mean_2 = np.mean(nl2d[2,2,(lmap>int(0.7*lmax)) & (lmap<int(lmax))])
                                 
                nl2d[0,0] /= mean_0
                nl2d[1,1] /= mean_1
                nl2d[2,2] /= mean_2

                nl2d = enmap.lform(nl2d)

                nl2d_sim = enmap.calc_ps2d(fmap_sim[:,None,:,:], fmap_sim[None,:,:,:])

                # Normalize to white noise floor of TOD sim
                nl2d_sim[0,0] /= mean_0
                nl2d_sim[1,1] /= mean_1
                nl2d_sim[2,2] /= mean_2

                nl2d_sim = enmap.lform(nl2d_sim)

                if freq in ('f030', 'f040'):
                    ticks = 250
                elif freq in ('f090', 'f150'):
                    ticks = 1000
                else:
                    ticks = 2000
                
                for idx in range(3):
                    for jdx in range(idx, 3):
                        nl2d[idx,jdx] = ndimage.gaussian_filter(nl2d[idx,jdx], 2)
                        nl2d_sim[idx,jdx] = ndimage.gaussian_filter(nl2d_sim[idx,jdx], 2)

                        if idx != 0 and jdx != 0:
                            lvmax = 2
                        else:
                            lvmax = 2.5
                        
                        if idx == jdx:
                            plot = enplot.plot(np.log10(np.abs(nl2d[idx,jdx])),
                                               colorbar=True, ticks=ticks,
                                               max=lvmax, min=-1, color=color,
                                               upgrade=upgrade)
                            enplot.write(
                                opj(imgdir,
                                    f'coadd_SAT_{freq}_2way_set0{sidx-1}_psd_log_{paidx}_{idx}_{jdx}'),
                                plot)

                            plot = enplot.plot(np.log10(np.abs(nl2d_sim[idx,jdx])),
                                               colorbar=True, ticks=ticks,
                                               max=lvmax, min=-1, color=color,
                                               upgrade=upgrade)
                            enplot.write(opj(imgdir,
                                    f'coadd_SAT_{freq}_2way_set0{sidx-1}_psd_log_sim_{paidx}_{idx}_{jdx}'),
                                    plot)

                        # Make sure data and sim get same color range.
                        pvmin, pvmax = (np.quantile(nl2d[idx,jdx], 0.03), np.quantile(nl2d[idx,jdx], 0.97))

                        plot = enplot.plot(nl2d[idx,jdx], colorbar=True,
                                           ticks=ticks, min=0, max=pvmax, upgrade=upgrade)
                        enplot.write(
                            opj(imgdir,
                                f'coadd_SAT_{freq}_2way_set0{sidx-1}_psd_{paidx}_{idx}_{jdx}'),
                            plot)

                        plot = enplot.plot(
                            nl2d_sim[idx,jdx], colorbar=True,
                            ticks=ticks, min=0, max=pvmax, upgrade=upgrade)
                        enplot.write(opj(imgdir,
                                f'coadd_SAT_{freq}_2way_set0{sidx-1}_psd_sim_{paidx}_{idx}_{jdx}'),
                                plot)
