import healpy as hp
import mapsims
from glob import glob
import pickle
import numpy as np
import sys
import pixell

tube = sys.argv[1]
m = {}
cl = []
folder = "output/noise/0000/"

sim = mapsims.from_config(
    ["common.toml", "noise.toml"], override={"channels": "tube:" + tube}
)
nside = mapsims.get_default_so_resolution(sim.channels[0])
lmax = 3*nside-1
noise = sim.other_components["noise"]
inverse_noise_variance = noise.get_inverse_variance(tube)
hitmap, _ = noise.get_hitmaps(tube)
pixarea_map = noise.pixarea_map

alm={}
for i, ch in enumerate(mapsims.parse_channels("tube:" + tube)[0]):
    hitmap[i] /= hitmap[i].max()

    filename = glob(folder + f"*{ch.tag}*1_of_1*")[0]
    print("reading " + filename)
    m[i] = pixell.enmap.read_map(filename)
    m[i][np.isnan(m[i])] = 0
    
    alm[i] = pixell.curvedsky.map2alm(
        np.sqrt(hitmap[i])*m[i], lmax=lmax
    )
    mask = hitmap[i] > 0
    sky_fraction = np.sum(mask*pixarea_map) /np.pi / 4.
    mean_hits = np.mean(hitmap[i])

    cl.append(
        hp.alm2cl(alm[i]) / sky_fraction / mean_hits
    )
cl.append(
    hp.alm2cl(alm[0], alm[1]) / sky_fraction / mean_hits
)

cl = np.array(cl)
with open(f"output/noise/N_ell_tube_{tube}.pkl", "wb") as f:
    pickle.dump(cl, f, protocol=-1)
