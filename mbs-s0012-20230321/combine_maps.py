import os
import healpy as hp
import numpy as np
from astropy.table import QTable
from pixell import enmap

# Dipole needs to be the last component, I remove dipole
# from previous map before adding dipole
all_combined = {
    "galactic_foregrounds_mediumcomplexity": [
        "dust",
        "synchrotron",
        "freefree",
        "ame",
        "co",
    ],
    "galactic_foregrounds_lowcomplexity": [
        "dust_low",
        "synchrotron_low",
        "freefree",
        "ame",
        "co_low",
    ],
    "galactic_foregrounds_highcomplexity": [
        "dust_high",
        "synchrotron_high",
        "freefree",
        "ame_high",
        "co",
    ],
    "combined_extragalactic": ["cib", "ksz", "tsz", "radio"],
}

chs = QTable.read(
    "simonsobs_instrument_parameters_2023.03/simonsobs_instrument_parameters_2023.03.tbl",
    format="ascii.ipac",
)

num = 0

#for pixelization in ["healpix", "car"]:
for pixelization in ["car"]:
    for tag, components in all_combined.items():
        for row in chs:
            band = row["band"]
            telescope = row["telescope"]
            output_folder = f"output/{tag}/"
            output_filename = (
                output_folder
                + f"sobs_mbs-s0012-20230321_{telescope}_mission_{band}_{tag}_{pixelization}.fits"
            )
            if not os.path.exists(output_filename):
                print(20 * "*")
                print("Starting")
                print(output_filename)
                for content in components:
                    print(content)
                    folder = f"output/{content}/"
                    filename = (
                        folder
                        + f"sobs_mbs-s0012-20230321_{telescope}_mission_{band}_{content}_{pixelization}.fits"
                    )
                    print("Read", filename)
                    if pixelization == "healpix":
                        m = hp.read_map(
                            filename, dtype=np.float64, field=(0, 1, 2), nest=True
                        )
                    else:
                        m = enmap.read_map(filename)
                    try:
                        combined_map += m
                    except NameError:
                        combined_map = m
                os.makedirs(os.path.dirname(output_filename), exist_ok=True)
                if pixelization == "healpix":
                    hp.write_map(
                        output_filename,
                        combined_map,
                        nest=True,
                        coord="C",
                        column_units="uK_CMB",
                        overwrite=True,
                        dtype=np.float32,
                    )
                else:
                    enmap.write_map(output_filename, combined_map)
                del combined_map
                print(20 * "*")
                print(output_filename)
                print(20 * "*")
