from make_gal_masks import *

thr = [1.0, 2.0, 3.0, 3.5, 4.0, 4.5]
inst = ['sa', 'la']
map_dir = '/global/cscratch1/sd/zonca/simonsobs/mapsims_runs/201904_highres_foregrounds_equatorial/' 
for t in thr:
	for i in inst:
		if i=='sa':
			nside = 512
		if i=='la':
			nside = 4096
		mask = make_mask(map_dir, inst=i, nside=nside, fsky=None, thr=t, pol=True)
		fsky = len(mask[mask>0])/float(len(mask))
		str_fsky = '{:04.2f}'.format(fsky)
		str_fsky = str_fsky.replace('.', 'p')
		str_thr = str(t).replace('.', 'p')
		file_name = './270519/mask_equatorial_pol_thr'+str_thr+'_fsky'+str_fsky+'_ns'+str(nside)+'.fits'
		hp.write_map(file_name, mask, overwrite=True)
