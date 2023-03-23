#!/bin/bash
#SBATCH --partition=cmbas
#SBATCH --nodes=1
#SBATCH --job-name=mapsims
#SBATCH --cpus-per-task=48
#SBATCH --time=24:0:00
#SBATCH --job-name=mapsims_synchrotron_low_LAT_f150
#SBATCH --error=logs/mapsims_synchrotron_low_LAT_f150_%j.err
#SBATCH --output=logs/mapsims_synchrotron_low_LAT_f150_%j.out

export OMP_NUM_THREADS=48
export NUMBA_NUM_THREADS=$OMP_NUM_THREADS

export PYTHONUNBUFFERED=1

time mapsims_run --verbose --channels='LAT_f150' common.toml synchrotron_low.toml
