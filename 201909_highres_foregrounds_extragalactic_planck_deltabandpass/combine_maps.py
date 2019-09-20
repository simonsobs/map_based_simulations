import os
import healpy as hp
import numpy as np

components = {
"201909_highres_foregrounds_extragalactic_planck_deltabandpass" : ["dust", "synchrotron", "freefree", "ame"] + ["cib", "ksz", "tsz", "cmb"],
}

num = 0

for nside in [512, 4096]:
    for telescope in ["planck"]:
        for band in ["030", "044", "070", "100", "143", "217", "545", "857"]:
            output_content = "combined"
            output_filename = f"{nside}/{output_content}/{num:04d}/simonsobs_{output_content}_uKCMB_{telescope}{band}_nside{nside}_{num:04d}.fits"
            if not os.path.exists(output_filename):
                combined_map = np.zeros((3, hp.nside2npix(nside)), dtype=np.float32)
                for release, contents in components.items():
                    for content in contents:
                        filename = f"/project/projectdirs/sobs/v4_sims/mbs/{release}/{nside}/{content}/{num:04d}/planck_deltabandpass_{content}_uKCMB_{telescope}{band}_nside{nside}_{num:04d}.fits"
                        print(filename)
                        try:
                            combined_map += hp.read_map(filename, dtype=np.float32, field=(0,1,2))
                        except IndexError:
                            print("T only map")
                            combined_map[0] += hp.read_map(filename, dtype=np.float32, field=0)
                os.makedirs(os.path.dirname(output_filename), exist_ok=True)
                combined_map = hp.reorder(combined_map, r2n=True)
                hp.write_map(output_filename, combined_map, nest=True, coord="C", column_units="uK_CMB", overwrite=True)
                print(20*"*")
                print(output_filename)
                print(20*"*")
