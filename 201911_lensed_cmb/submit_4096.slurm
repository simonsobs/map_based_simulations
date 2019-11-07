#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=14:00:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims_cmb_4096
#SBATCH --error=mapsims_cmb_4096_%j.err
#SBATCH --output=mapsims_cmb_4096_%j.out
#SBATCH --array=0-99

time mapsims_run --nside 4096 --channels all --num $SLURM_ARRAY_TASK_ID ../common.toml ../cmb.toml
