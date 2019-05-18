#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=5:30:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims_dust_512_all
#SBATCH --error=mapsims_dust_512_all_%j.err
#SBATCH --output=mapsims_dust_512_all_%j.out

time mapsims_run --nside 512 --channels all ../common.toml ../dust_512.toml
