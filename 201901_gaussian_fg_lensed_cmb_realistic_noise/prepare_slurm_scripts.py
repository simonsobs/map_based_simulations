from pathlib import Path

template = open("submit.slurm").read()
foregrounds = ["dust", "synchrotron"]

for nside in [4096, 512]:
    highres = nside == 4096
    for simulation_type in ["dust", "synchrotron", "noise", "cmb"]:
        folder = Path(f"output/{nside}/{simulation_type}")
        folder.mkdir(exist_ok=True)
        hours = 2 if highres and simulation_type in foregrounds else 1
        minutes = 30
        last_sim_id = 9 if highres else 109
        if (not highres) and (simulation_type in foregrounds):
            last_sim_id = 10
        with open(folder / "submit.slurm", "w") as f:
            print("writing", f.name)
            f.write(template.format(
                simulation_type=simulation_type,
                nside=nside,
                hours=hours,
                minutes=minutes,
                channels="all" if highres else "SA",
                #channels="'SA_27,LA_27'",
                first_sim_id=0 if highres else 10,
                last_sim_id=last_sim_id
            ))
