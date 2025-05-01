import os
import sys
import healpy as hp
import numpy as np
from astropy.table import QTable
from pixell import enmap
import toml
import glob

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

all_combined = {**all_combined, **new_combined}


chs = QTable.read(
    "instrument_model/instrument_model.tbl",
    format="ascii.ipac",
)

pixelizations = ["healpix"]

# Load the common.toml file
with open("common.toml", "r") as f:
    common_config = toml.load(f)

try:
    output_folder_template = common_config["output_folder"]
    template = common_config["output_filename_template"]
except KeyError as e:
    raise KeyError(f"{e.args[0]} not found in common.toml")

for pixelization in pixelizations:
    for tag, components in all_combined.items():
        for row in chs:
            band = row["band"]
            telescope = row["telescope"]

            # Build output folder and filename from templates
            output_folder = output_folder_template.format(tag=tag)
            output_filename = os.path.join(
                output_folder,
                template.format(
                    tag=tag,
                    telescope=telescope,
                    band=band,
                    pixelization=pixelization,
                ),
            )

            if not os.path.exists(output_filename):
                print(20 * "*")
                print("Starting")
                print(output_filename)
                for content in components:
                    print(content)
                    folder = f"output/{content}/"
                    pattern = (
                        folder
                        + f"*_{telescope}_mission_{band}_{content}_{pixelization}.fits"
                    )
                    matches = glob.glob(pattern)
                    if not matches:
                        print(f"File not found: {pattern}")
                        continue
                    filename = matches[0]

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
                output_dir = os.path.dirname(output_filename)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
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
