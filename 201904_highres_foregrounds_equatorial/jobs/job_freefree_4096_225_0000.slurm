#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=5:30:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims_freefree_4096_225
#SBATCH --mail-user
#SBATCH --error=mapsims_freefree_4096_%j.err
#SBATCH --output=mapsims_freefree_4096_%j.out

time mapsims_run --nside 4096 --channels 225 ../common.toml ../freefree_4096.toml
