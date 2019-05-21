#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=5:30:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims_cmb_4096_027
#SBATCH --error=mapsims_cmb_4096_027_%j.err
#SBATCH --output=mapsims_cmb_4096_027_%j.out

time mapsims_run --nside 4096 --channels 027 ../common.toml ../cmb.toml
