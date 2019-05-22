#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=5:30:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims_tsz_4096_093
#SBATCH --error=mapsims_tsz_4096_093_%j.err
#SBATCH --output=mapsims_tsz_4096_093_%j.out

time mapsims_run --nside 4096 --channels 093 ../common.toml ../tsz.toml
