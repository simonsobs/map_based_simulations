#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=5:30:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims_freefree_512
#SBATCH --mail-user
#SBATCH --error=mapsims_freefree_512_%j.err
#SBATCH --output=mapsims_freefree_512_%j.out

time mapsims_run ../common_512.toml ../freefree_512.toml
