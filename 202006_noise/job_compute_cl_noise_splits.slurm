#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=5:30:00
#SBATCH --nodes=1
#SBATCH --job-name=compute_cl_splits
#SBATCH --error=log_compute_cl_splits_%j.err
#SBATCH --output=log_compute_cl_splits_%j.out
#SBATCH --ntasks-per-node=48
#SBATCH --array=0-6

export OMP_NUM_THREADS=48
export PYTHONUNBUFFERED=1

python compute_cl_noise_splits.py LT$SLURM_ARRAY_TASK_ID
