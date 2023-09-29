'''
Reproject the HEALPIX maps to CAR maps. Also defines "mask_obs", which 
defindes what pixels are given to mnms.
'''
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import os
import numpy as np

import healpy as hp
from pixell import enmap, enplot, reproject, utils, curvedsky
from optweight import mat_utils, map_utils

opj = os.path.join

mapdir = '/mnt/home/aduivenvoorden/project/so/20230524_sat_noise/v1'
imgdir = opj(mapdir, 'img_car')
cardir = opj(mapdir, 'car')
maskdir = opj(cardir, 'masks')
odir = opj(mapdir, 'car')

os.makedirs(imgdir, exist_ok=True)

def construct_f1_geometry(box, res):
    '''
    Parameters
    ----------
    box : (2, 2) array
        [{from,to},{dec,ra}] array giving the bottom-left and top-right corners of the desired geometry
        in degrees.
    res : float
        Resolution in arcmin / pixel.

    Returns
    -------
    shape : tuple
        Shape of geometry.
    wcs : astropy.wcs.WCS object
        WCS of geometry.
    '''
    
    box = np.radians(np.asarray(box))
    shape, wcs = enmap.geometry(box, res=res * utils.arcmin, proj='CAR')

    if wcs.wcs.cdelt[0] > 0:
        raise ValueError(
            f'By convention the X CDELT value should be negative, got : {wcs.wcs.cdelt[0]}')
    if wcs.wcs.cdelt[1] < 0:
        raise ValueError(
            f'By convention the Y CDELT value should be positive, got : {wcs.wcs.cdelt[1]}')

    # Check if geometry conforms to Clenshaw–Curtis. This will raise error if no quad rule can be found.
    # This should never happen because the above always creates CC CAR maps.
    curvedsky.get_minfo(shape, wcs, quad=True)

    # Convert Clenshaw–Curtis CAR map to a Feyer1 CAR map.
    wcs.wcs.crpix[1] -= 0.5

    # Check if input map included the north pole, if so, we need to subtract one row.
    # We do this by checking if the y pixel center of the top corner of the map has been shifted
    # above +90 deg.
    if np.degrees(enmap.corners(shape, wcs, corner=False))[1,0] > 90:
        shape = (shape[0] - 1, shape[1])
        
    # Check if geometry conforms to Feyer1. 
    curvedsky.get_minfo(shape, wcs, quad=True)

    return shape, wcs

freqs = ['f030', 'f040', 'f090', 'f150', 'f230', 'f290']
box = np.asarray([[-75, 180],[35,-180]])

# These resolution numbers are determined by taking lmax = 3 x nside
# and then adding a factor 2 again, which is currently needed for mnmns,
# and then adding slightly more pixels to allow for quadrature in the CAR maps.
geom_dict = {'f030' : {'box' : box, 'res' : 40 / 3},
             'f040' : {'box' : box, 'res' : 40 / 3},
             'f090' : {'box' : box, 'res' : 10 / 3},
             'f150' : {'box' : box, 'res' : 10 / 3},
             'f230' : {'box' : box, 'res' : 5 / 3},
             'f290' : {'box' : box, 'res' : 5 / 3}
             }
nside_dict = {'f030' : 128, 'f040' : 128, 'f090' : 512, 'f150' : 512, 'f230' : 1024, 'f290' : 1024}

freq_pairs = [('f030', 'f040'), ('f090', 'f150'), ('f230', 'f290')]

for pair in freq_pairs:

    mask_obs = None
    
    for freq in pair:

        box = geom_dict[freq]['box']
        res = geom_dict[freq]['res']
        
        shape, wcs = construct_f1_geometry(box, res)
    
        font_size = 20 if freq in ('f030', 'f040') else 60

        # Construct a CAR version of mask_obs. Masking the noisiest pixels.        
        for sidx in range(1, 3):

            icov = hp.read_map(
                opj(mapdir, f'coadd_SAT_{freq}_00{sidx}of002_invcov.fits'),
                field=None)
            icov[icov == hp.UNSEEN] = 0
            icov *= 1e-12

            ivar = np.zeros((3, icov.shape[-1]), dtype=icov.dtype)
            ivar[0] = icov[0]
            ivar[1] = icov[3]
            ivar[2] = icov[5]

            ivar = reproject.healpix2map(ivar, shape=shape, wcs=wcs, extensive=True,
                                                 method='spline', order=1, spin=0)

            ivar_1d = ivar.reshape(3, np.prod(ivar.shape[-2:]))            
            ivar_1d = map_utils.round_icov_matrix(ivar_1d, rtol=1e-3)
            ivar_tr = enmap.samewcs(ivar_1d.reshape(*ivar.shape), ivar)

            fig, axs = plt.subplots(dpi=300, nrows=3)
            for pidx in range(3):
                axs[pidx].hist(np.log10(ivar[pidx][ivar[pidx] != 0]), bins=1000)
                axs[pidx].hist(np.log10(ivar_tr[pidx][ivar_tr[pidx] != 0]), bins=1000)
                axs[pidx].set_yscale('log')
            fig.savefig(opj(imgdir, f'coadd_SAT_{freq}_00{sidx}of002_ivar_hist'))
            plt.close()

            cut = ivar - ivar_tr
            cut = cut.astype(bool)
            cut = np.sum(cut, axis=0).astype(np.int32)

            plot = enplot.plot(cut, colorbar=True, ticks=30,
                               font_size=font_size)
            enplot.write(opj(imgdir, f'coadd_SAT_{freq}_00{sidx}of002_cut'), plot)

            if mask_obs is None:                
                mask_obs = np.prod(ivar_tr.astype(bool), axis=0)
            else:
                mask_obs *= np.prod(ivar_tr.astype(bool), axis=0)

    # We use a common mask between two frequencies on the same array and also I, Q, U.
    mask_obs = mask_obs.astype(bool)
    mask_obs = mask_obs.astype(np.float32)

    plot = enplot.plot(mask_obs, colorbar=True, ticks=30,
                       font_size=font_size)
    enplot.write(opj(imgdir, f'coadd_SAT_{pair[0]}_{pair[1]}_mask_obs'), plot)
                
    enmap.write_map(opj(maskdir, f'coadd_SAT_{pair[0]}_{pair[1]}_mask_obs.fits'), mask_obs)

    # Also save a HEALPix version.
    mask_obs_hp = reproject.map2healpix(mask_obs, nside=nside_dict[freq], extensive=False,
                                 method='spline', order=1, spin=0)
    mask_obs_hp[mask_obs_hp < 1] = 0

    fig, ax = plt.subplots(dpi=300)
    plt.axes(ax)
    hp.mollview(mask_obs_hp, hold=True, min=-0.5, max=1.5)
    fig.savefig(opj(imgdir, f'coadd_SAT_{pair[0]}_{pair[1]}_mask_obs_hp.png'))
    plt.close(fig)                
    
    hp.write_map(opj(maskdir, f'coadd_SAT_{pair[0]}_{pair[1]}_mask_obs_hp.fits'), mask_obs_hp,
                 overwrite=True)
    
    for freq in pair:

        for sidx in range(1, 3):

            mapname = f'coadd_SAT_{freq}_00{sidx}of002_map'
            imap = hp.read_map(
                opj(mapdir, mapname + '.fits'),
                field=None)
            imap[imap == hp.UNSEEN] = 0            
            imap = np.atleast_2d(imap)
            imap *= 1e6
            nside = hp.npix2nside(imap.shape[-1])
            lmax = 2.5 * nside

            # Load up ivar. We only do ivar, because unclear how to correctly
            # interpolate all elements of div (i.e. they don't have well-defined
            # spin; probably not important, but this seems safer).
            # We alos convert all maps to uK units (input is in K).
            ivarname = f'coadd_SAT_{freq}_00{sidx}of002_invcov'
            ivar = hp.read_map(
                opj(mapdir, ivarname + '.fits'),
                field=[0])
            ivar[ivar == hp.UNSEEN] = 0                        
            ivar *= 1e-12
            ivar = np.atleast_2d(ivar)

            # One extensive=True ivar map to write to disk.
            omap_ivar_ex = reproject.healpix2map(ivar, shape=shape, wcs=wcs, extensive=True,
                                                 method='spline', order=1)
                        
            font_size = 20 if freq in ('f030', 'f040') else 60

            # For visual comparison, reproject map using nearest-neighbor.
            omap_spline = reproject.healpix2map(imap, shape=shape, wcs=wcs, extensive=False,
                                                method='spline', order=0)

            # Flatten map before reprojection to avoid ringing from noisy edges.
            sqrt_ivar = mat_utils.matpow(ivar, 0.5, return_diag=True)
            imap_flat = imap * sqrt_ivar

            # Reproject weighted map.        
            omap = reproject.healpix2map(imap_flat, shape=shape, wcs=wcs, extensive=False,
                                         method='harm', lmax=lmax)

            # Reproject the ivar. Note that we do not use extensive=True, because we
            # also did not do that for the flattened map.
            omap_ivar = reproject.healpix2map(ivar, shape=shape, wcs=wcs, extensive=False,
                                              method='spline', order=1)

            # Unwhiten map.
            omap_ivar_flat = omap_ivar.reshape((1, np.prod(omap_ivar.shape[-2:])))
            isqrt_ivar = mat_utils.matpow(omap_ivar_flat, -0.5, return_diag=True)
            isqrt_ivar = isqrt_ivar.reshape((1,) + omap.shape[-2:])
            omap *= isqrt_ivar                                           

            # Write maps to disk. Note that we change to 0-indexing and rename invcov to ivar
            # to make mnms extra happy. We follow the tod2map_docs recommended file formatting:
            # https://simons1.princeton.edu/docs/tod2maps_docs/ \
            # analysis_interface/analysis_interface_LATEST.pdf
            mapname2write = f'coadd_SAT_{freq}_2way_set{sidx-1:02d}_map'
            enmap.write_fits(opj(odir, f'{mapname2write}.fits'), omap)
            ivarname2write = mapname2write.replace('map', 'ivar')
            enmap.write_fits(opj(odir, f'{ivarname2write}.fits'), omap_ivar_ex)

            # Plot maps.
            npol = omap.shape[0]
            tmin, tmax = (np.quantile(omap[0], 0.01), np.quantile(omap[0], 0.99))
            pmin, pmax = (np.quantile(omap[1], 0.01), np.quantile(omap[1], 0.99))
            vmin = [tmin, pmin, pmin]
            vmax = [tmax, pmax, pmax]

            for pidx in range(npol):
                plot = enplot.plot(omap[pidx], colorbar=True, ticks=30, min=vmin[pidx], max=vmax[pidx],
                                   font_size=font_size)
                enplot.write(opj(imgdir, f'{mapname}_{pidx}'), plot)

            for pidx in range(npol):
                plot = enplot.plot(omap_spline[pidx], colorbar=True, ticks=30,
                                   min=vmin[pidx], max=vmax[pidx],
                                   font_size=font_size)
                enplot.write(opj(imgdir, f'{mapname}_spline_{pidx}'), plot)

            for pidx in range(npol):
                plot = enplot.plot(omap[pidx] - omap_spline[pidx], colorbar=True, ticks=30,
                                   min=vmin[pidx], max=vmax[pidx], font_size=font_size)
                enplot.write(opj(imgdir, f'{mapname}_diff_{pidx}'), plot)

            plot = enplot.plot(omap_ivar, colorbar=True, ticks=30)
            enplot.write(opj(imgdir, f'{ivarname}'), plot)
