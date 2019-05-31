import healpy as hp
import numpy as np

def smooth_mask(mask, fwhm=10., l=0.5):
	mask = hp.smoothing(mask, np.radians(fwhm))
	lim=max(mask)*l
	mask[mask > lim]=1
	mask[mask <= lim]=0
	return mask

def smooth_and_udgrade(map_in, nside=512, inst='sa'):
	if inst=='sa':
		fwhm_rad = np.radians(np.sqrt(60.**2-30**2.)/60.)
	if inst=='la':
		fwhm_rad = np.radians(np.sqrt(60.**2-2.2**2.)/60.)
	map_in = hp.smoothing(map_in, fwhm = fwhm_rad)
	map_in = hp.ud_grade(map_in, nside)
	return map_in

def make_fg_map(map_dir, inst='sa', nside=512):
	if nside<=512:
		dir_fg = map_dir+'512/'
	else:
		dir_fg = map_dir+'4096/'
	fgs = ['dust', 'synchrotron', 'ame', 'freefree']
	map_fg_tot = np.zeros((3, hp.nside2npix(nside)))
	for fg in fgs:
		map_file = dir_fg+fg+'/0000/simonsobs_'+fg+'_uKCMB_'+inst+'093_nside'+str(nside)+'_0000.fits'
		try:
			fg_map = hp.read_map(map_file, (0,1,2))
		except:
			fg_map = hp.read_map(map_file)
			fg_map = np.array((fg_map, fg_map*0., fg_map*0.))
		map_fg_tot += fg_map
	map_fg_tot = smooth_and_udgrade(map_fg_tot, nside=nside, inst=inst)
	return map_fg_tot

def return_CMB_thr(nside=512, inst='sa'):
	cmb_dir = '/global/cscratch1/sd/zonca/simonsobs/mapsims_runs/201901_gaussian_fg_lensed_cmb_realistic_noise/'+str(nside)+'/cmb/'
	if nside<=512:
		cmb = hp.read_map(cmb_dir+'0010/simonsobs_cmb_uKCMB_'+inst+'093_nside512_0010.fits', (0,1,2))
	else:
		cmb = hp.read_map(cmb_dir+'0000/simonsobs_cmb_uKCMB_'+inst+'093_nside4096_0000.fits', (0,1,2))
	cmb = smooth_and_udgrade(cmb, nside=nside, inst=inst)
	stdT = np.std(cmb[0])
	stdQ = np.std(cmb[1])
	stdU = np.std(cmb[2])
	return stdT, stdQ, stdU

def make_mask(map_dir, inst='sa', nside=512, fsky=0.5, thr=None, pol=True):
	fg_map = make_fg_map(map_dir, inst=inst, nside=nside)
	mask = np.copy(fg_map[0])*0.
	if fsky:
		if pol:
			fg_map_to_use = fg_map[1]**2.+fg_map[2]**2.
		if pol==False:
			fg_map_to_use = fg_map[0]
		fg_map_reord = np.sort(fg_map_to_use)
		ind_cut = int(fsky*len(fg_map_reord))
		value = fg_map_reord[ind_cut]
		mask_out = np.copy(mask)*0.
		mask_out[fg_map_to_use<value] = 1.
	if thr:
		stdT, stdQ, stdU = return_CMB_thr(nside=nside, inst=inst)
		if pol:
			maskQ = np.copy(mask)*0.+1
			maskU = np.copy(mask)*0.+1
			maskQ[np.abs(fg_map[1])>thr*stdQ] = 0
			maskU[np.abs(fg_map[2])>thr*stdU] = 0
			mask_out = maskQ*maskU
		if pol==False:
			mask_out = np.copy(mask)*0.+1
			mask_out[fg_map[0]>thr*stdT] = 0
	mask_out = smooth_mask(mask_out, 10.)
	return mask_out
		
		
		
		
	
	


		
