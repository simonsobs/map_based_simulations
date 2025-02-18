import healpy as hp
import sys
from glob import glob
import pickle
import h5py
import os.path
from astropy.table import QTable
import toml

# Read the common.toml file
config = toml.load("common.toml")

chs = QTable.read(
    config["instrument_parameters"],
    format="ascii.ipac",
)

if len(sys.argv) > 1:
    folder = sys.argv[1]
else:
    ID = int(os.environ["SLURM_ARRAY_TASK_ID"])
    folder = [f for f in glob("output/*") if (not f.endswith("pkl") and not f.endswith("C_ell"))][ID]
print(folder)
component = os.path.basename(folder)

output_filename = f"output/C_ell/C_ell_{component}.pkl"
if os.path.exists(output_filename):
    print(f"{output_filename} already exists")
    sys.exit(0)

cl = {}
for ch in chs:
    try:
        filename = config["output_filename_template"].format(
            tag=component,
            telescope="PICO",
            band=ch["band"],
            pixelization="healpix"
        )
        filename = os.path.join(folder, filename)
    except IndexError:
        print(folder + f"*{ch['band']}* NOT FOUND " + ("*" * 20))
        break
    print("reading " + filename)
    try:
        m = hp.read_map(filename, (0, 1, 2))
        nside = hp.npix2nside(len(m[0]))
    except:
        m = hp.read_map(filename)
        nside = hp.npix2nside(len(m))

    cl[ch["band"]] = hp.anafast(m, lmax=int(2.5 * nside), use_pixel_weights=False)

if cl:  # empty dicts are false
    with open(output_filename, "wb") as f:
        pickle.dump(cl, f, protocol=-1)
