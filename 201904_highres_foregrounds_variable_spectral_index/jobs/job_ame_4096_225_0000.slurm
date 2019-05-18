#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=5:30:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims_ame_4096_225
#SBATCH --error=mapsims_ame_4096_225_%j.err
#SBATCH --output=mapsims_ame_4096_225_%j.out

time mapsims_run --nside 4096 --channels 225 ../common.toml ../ame_4096.toml
