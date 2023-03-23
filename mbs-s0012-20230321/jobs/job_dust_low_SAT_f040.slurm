#!/bin/bash
#SBATCH --partition=cmbas
#SBATCH --nodes=1
#SBATCH --job-name=mapsims
#SBATCH --cpus-per-task=48
#SBATCH --time=24:0:00
#SBATCH --job-name=mapsims_dust_low_SAT_f040
#SBATCH --error=logs/mapsims_dust_low_SAT_f040_%j.err
#SBATCH --output=logs/mapsims_dust_low_SAT_f040_%j.out

export OMP_NUM_THREADS=48
export NUMBA_NUM_THREADS=$OMP_NUM_THREADS

export PYTHONUNBUFFERED=1

time mapsims_run --verbose --channels='SAT_f040' common.toml dust_low.toml
