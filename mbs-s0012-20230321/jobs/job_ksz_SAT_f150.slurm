#!/bin/bash
#SBATCH --partition=cmbas
#SBATCH --nodes=1
#SBATCH --job-name=mapsims
#SBATCH --cpus-per-task=48
#SBATCH --time=24:0:00
#SBATCH --job-name=mapsims_ksz_SAT_f150
#SBATCH --error=logs/mapsims_ksz_SAT_f150_%j.err
#SBATCH --output=logs/mapsims_ksz_SAT_f150_%j.out

export OMP_NUM_THREADS=48
export NUMBA_NUM_THREADS=$OMP_NUM_THREADS

export PYTHONUNBUFFERED=1

time mapsims_run --verbose --channels='SAT_f150' common.toml ksz.toml
