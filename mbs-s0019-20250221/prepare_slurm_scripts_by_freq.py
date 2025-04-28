from pathlib import Path
import sys
import os
import subprocess

folder = Path(f"jobs")
folder.mkdir(exist_ok=True, parents=True)

from glob import glob

sims = list(glob("*.toml"))
sims = [s.split(".")[0] for s in sims]
sims.remove("common")
sims = ["radio_rg1", "radio_rg2", "radio_rg3"]

from mapsims.channel_utils import parse_channels

import toml

config = toml.load("common.toml")

chs = parse_channels(instrument_parameters=config["instrument_parameters"])
max_jobs = 500
i_job = 1
for simulation_type in sims:
    os.makedirs(config["output_folder"].format(tag=simulation_type), exist_ok=True)
    config_file = simulation_type
    template = open("submit.slurm").read()
    hours = 48
    minutes = 00
    for channel in chs:
        output_filename = (
            config["output_folder"] + "/" + config["output_filename_template"]
        ).format(
            tag=simulation_type,
            telescope=channel.telescope,
            band=channel.band,
            nside=channel.nside,
            pixelization="healpix"
        )
        if os.path.exists(output_filename):
            print("SKIP", output_filename)
        else:
            tag = channel.tag.replace(" ", "_")
            filename = f"job_{simulation_type}_{tag}.slurm"
            with open(folder / filename, "w") as f:
                print(f"sbatch jobs/{filename} &")
                f.write(
                    template.format(
                        simulation_type=simulation_type,
                        hours=hours,
                        minutes=minutes,
                        channels=tag,
                        run_channels=tag,
                        config_file=config_file,
                    )
                )

            subprocess.run(["sbatch", f"jobs/{filename}"])
            if i_job == max_jobs:
                print(f"Submitted {max_jobs} jobs")
                sys.exit(0)
            i_job += 1

