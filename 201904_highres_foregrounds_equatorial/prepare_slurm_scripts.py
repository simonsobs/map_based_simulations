from pathlib import Path

template = open("submit.slurm").read()
folder = Path(f"jobs")
folder.mkdir(exist_ok=True, parents=True)

print("cd jobs")
for nside in [512, 4096]:
    for simulation_type in ["dust", "synchrotron", "freefree", "ame"]:
        hours = 5
        minutes = 30
        num = 0
        filename = f"job_{simulation_type}_{nside}_{num:04d}.slurm"
        with open(folder / filename, "w") as f:
            print("sbatch", filename)
            f.write(template.format(
                simulation_type=simulation_type,
                nside=nside,
                hours=hours,
                minutes=minutes,
                channels="all",
                first_sim_id=0,
                last_sim_id=0
            ))
