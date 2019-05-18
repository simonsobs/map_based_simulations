#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=5:30:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims_synchrotron_512_all
#SBATCH --mail-user
#SBATCH --error=mapsims_synchrotron_512_%j.err
#SBATCH --output=mapsims_synchrotron_512_%j.out

time mapsims_run --nside 512 --channels all ../common.toml ../synchrotron_512.toml
