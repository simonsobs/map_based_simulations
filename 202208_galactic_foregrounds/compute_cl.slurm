#!/bin/bash
#SBATCH --partition=cmbas
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --job-name=compute_cl
#SBATCH --error=logs/compute_cl_%j.out
#SBATCH --output=logs/compute_cl_%j.out
#SBATCH --cpus-per-task=48
#SBATCH --array=0-16

export OMP_NUM_THREADS=48
export NUMBA_NUM_THREADS=$OMP_NUM_THREADS
export HDF5_USE_FILE_LOCKING=FALSE
export PYTHONUNBUFFERED=1

time python compute_cl.py
