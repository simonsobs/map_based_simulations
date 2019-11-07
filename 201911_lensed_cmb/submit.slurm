#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=05:00:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims_cmb
#SBATCH --error=mapsims_cmb_%j.err
#SBATCH --output=mapsims_cmb_%j.out
#SBATCH --array=0-99

time mapsims_run --nside 512 --channels all --num $SLURM_ARRAY_TASK_ID ../common.toml ../cmb.toml
