from pathlib import Path

template = open("submit.slurm").read()

for nside in [4096]:
    for simulation_type in ["dust", "synchrotron", "freefree", "ame"]:
        folder = Path(f"output/{nside}/{simulation_type}")
        folder.mkdir(exist_ok=True, parents=True)
        hours = 2
        minutes = 30
        with open(folder / "submit.slurm", "w") as f:
            print("writing", f.name)
            f.write(template.format(
                simulation_type=simulation_type,
                nside=nside,
                hours=hours,
                minutes=minutes,
                channels="all",
                first_sim_id=0,
                last_sim_id=0
            ))
