import healpy as hp
import mapsims
from glob import glob
import pickle
import numpy as np
import sys

ellmax = int(1e4)
tube = sys.argv[1]
m = {}
cl = []
folder = "output/noise/0000/"
for i, ch in enumerate(mapsims.parse_channels("tube:"+tube)[0]):
    filename = glob(folder + f"*{ch.tag}*1_of_1*")[0]
    print("reading " + filename)
    m[i] = hp.read_map(filename, (0,1,2))
    npix = len(m[i][0])
    nside = hp.npix2nside(npix)
    sky_fraction=(m[i][0]>-1e30).sum()/npix
    cl.append(np.array(hp.anafast(m[i], lmax=min(3*nside-1,ellmax), use_pixel_weights=True)) / sky_fraction)
cl.append(np.array(hp.anafast(m[0],m[1], lmax=min(3*nside-1,ellmax), use_pixel_weights=True)) / sky_fraction)

cl = np.array(cl)
with open(f"output/noise/N_ell_tube_{tube}.pkl", "wb") as f:
    pickle.dump(cl, f, protocol=-1)
