from pathlib import Path

template = open("submit.slurm").read()
folder = Path(f"jobs")
folder.mkdir(exist_ok=True, parents=True)

print("cd jobs")
for nside in [512, 4096]:
    for simulation_type in ["cib", "ksz", "tsz"]:
        hours = 5
        minutes = 30
        num = 0
        freqs = ["{:03d}".format(f) for f in [27, 39, 93, 145, 225, 280]] if nside == 4096 else ["all"]
        for freq in freqs:
            filename = f"job_{simulation_type}_{nside}_{freq}_{num:04d}.slurm"
            channels = freq
            with open(folder / filename, "w") as f:
                print("sbatch", filename)
                f.write(template.format(
                    simulation_type=simulation_type,
                    nside=nside,
                    hours=hours,
                    minutes=minutes,
                    channels=channels,
                    freq=freq,
                    first_sim_id=0,
                    last_sim_id=0
                ))
