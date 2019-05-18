#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=5:30:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims_ame_4096_039
#SBATCH --mail-user
#SBATCH --error=mapsims_ame_4096_%j.err
#SBATCH --output=mapsims_ame_4096_%j.out

time mapsims_run --nside 4096 --channels 039 ../common.toml ../ame_4096.toml
