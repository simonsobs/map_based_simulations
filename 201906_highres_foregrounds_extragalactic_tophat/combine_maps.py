import os
import healpy as hp
import numpy as np

components = {
"201906_highres_foregrounds_extragalactic_tophat" : ["dust", "synchrotron", "freefree", "ame"],
"201906_highres_foregrounds_extragalactic_tophat" : ["cib", "ksz", "tsz", "cmb_lensed_solardipole"],
}

num = 0

for nside in [512, 4096]:
    for telescope in ["la", "sa"]:
        for band in ["LF1", "LF2", "MFF1", "MFF2", "MFS1", "MFS2", "UHF1", "UHF2"]:
            output_content = "combined_solardip"
            output_filename = f"{nside}/{output_content}/{num:04d}/simonsobs_{output_content}_uKCMB_{telescope}{band}_nside{nside}_{num:04d}.fits"
            if not os.path.exists(output_filename):
                combined_map = np.zeros((3, hp.nside2npix(nside)), dtype=np.float32)
                for release, contents in components.items():
                    for content in contents:
                        filename = f"/project/projectdirs/sobs/v4_sims/mbs/{release}/{nside}/{content}/{num:04d}/simonsobs_{content}_uKCMB_{telescope}{band}_nside{nside}_{num:04d}.fits"
                        print(filename)
                        if band == "LF1" and content == "cib":
                            continue
                        m = hp.read_map(filename, dtype=np.float32)
                        if m.shape[0] != 3:
                            combined_map[0] += m
                            print("T only map")
                        else:
                            assert m.shape == combined_map.shape
                            combined_map += m
                os.makedirs(os.path.dirname(output_filename), exist_ok=True)
                hp.write_map(output_filename, combined_map, nest=True, coord="C", column_units="uK_CMB", overwrite=True)
                print(20*"*")
                print(output_filename)
                print(20*"*")
