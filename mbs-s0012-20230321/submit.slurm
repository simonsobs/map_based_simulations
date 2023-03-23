#!/bin/bash
#SBATCH --partition=cmbas
#SBATCH --nodes=1
#SBATCH --job-name=mapsims
#SBATCH --cpus-per-task=48
#SBATCH --time={hours}:{minutes}:00
#SBATCH --job-name=mapsims_{simulation_type}_{channels}
#SBATCH --error=logs/mapsims_{simulation_type}_{channels}_%j.err
#SBATCH --output=logs/mapsims_{simulation_type}_{channels}_%j.out

export OMP_NUM_THREADS=48
export NUMBA_NUM_THREADS=$OMP_NUM_THREADS

export PYTHONUNBUFFERED=1

time mapsims_run --verbose --channels='{run_channels}' common.toml {config_file}.toml
