# IPython log file

import healpy as hp
import numpy as np
nside=4096
npix=hp.nside2npix(nside)
m=np.zeros((3,npix), dtype=np.float64)
mu=hp.ud_grade(m, 8192)
