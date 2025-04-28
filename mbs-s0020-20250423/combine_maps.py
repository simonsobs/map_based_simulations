import os
import sys
import healpy as hp
import numpy as np
from astropy.table import QTable
from pixell import enmap

all_combined = {
    "galactic_foregrounds_mediumcomplexity": [
        "dust_d10",
        "synchrotron_s5",
        "freefree_f1",
        "ame_a1",
        "co_co3",
    ],
    "galactic_foregrounds_d1s1": [
        "dust_d1",
        "synchrotron_s1",
    ],
    "galactic_foregrounds_lowcomplexity": [
        "dust_d9",
        "synchrotron_s4",
        "freefree_f1",
        "ame_a1",
        "co_co1",
    ],
    "galactic_foregrounds_highcomplexity": [
        "dust_d12",
        "synchrotron_s7",
        "freefree_f1",
        "ame_a2",
        "co_co3",
    ],
}

websky_catalog = ["tsz_tsz1", "ksz_ksz1", "radio_rg3", "radio_rg2", "cib_cib1"]

new_combined = {}
for name, components in all_combined.items():
    if name.startswith("galactic") and "d1s1" not in name:
        new_combined[name + "_websky"] = components + websky_catalog

all_combined = new_combined


chs = QTable.read(
    "instrument_model/instrument_model.tbl",
    format="ascii.ipac",
)

pixelizations = ["healpix"]

for pixelization in pixelizations:
    for tag, components in all_combined.items():
        for row in chs:
            band = row["band"]
            telescope = row["telescope"]
            output_folder = f"output/{tag}/"
            output_filename = (
                output_folder
                + f"sobs_mbs-s0020-20250423_{telescope}_mission_{band}_{tag}_{pixelization}.fits"
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
                        + f"*_{telescope}_mission_{band}_{content}_{pixelization}.fits"
                    )[0]

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
