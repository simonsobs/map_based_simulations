#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=5:30:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims_ame_4096
#SBATCH --mail-user
#SBATCH --error=mapsims_ame_4096_%j.err
#SBATCH --output=mapsims_ame_4096_%j.out

time mapsims_run ../common_4096.toml ../ame_4096.toml
