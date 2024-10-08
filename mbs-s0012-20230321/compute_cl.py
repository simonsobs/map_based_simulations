import healpy as hp
from glob import glob
import pickle
import h5py

import os.path

from astropy.table import QTable

ID = int(os.environ["SLURM_ARRAY_TASK_ID"])

chs = QTable.read(
    "simonsobs_instrument_parameters_2023.03/simonsobs_instrument_parameters_2023.03.tbl",
    format="ascii.ipac",
)
folder = [f for f in glob("output/*") if not f.endswith("pkl")][ID]
cl = {}
print(folder)
component = os.path.basename(folder)

output_filename = f"output/C_ell_{component}.pkl"
if os.path.exists(output_filename):
    print(f"{output_filename} already exists")
    sys.exit(0)

for ch in chs:
    try:
        filename_template = folder + f"/*{ch['telescope']}*{ch['band']}*healpix*"
        filename = glob(filename_template)[0]
    except IndexError:
        print(filename_teamplate + " NOT FOUND " + ("*" * 20))
        break
    print("reading " + filename)
    try:
        m = hp.read_map(filename, (0, 1, 2))
        nside = hp.npix2nside(len(m[0]))
    except:
        m = hp.read_map(filename)
        nside = hp.npix2nside(len(m))

    # if m.shape[0] == 3 and m[1].sum() == 0:
    #    m = m[0]

    cl[ch["tag"]] = hp.anafast(m, lmax=int(2.5 * nside), use_pixel_weights=False)

if cl:  # empty dicts are false
    with open(output_filename, "wb") as f:
        pickle.dump(cl, f, protocol=-1)
