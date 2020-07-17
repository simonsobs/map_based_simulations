#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=1:30:00
#SBATCH --nodes=1
#SBATCH --job-name=compute_cl
#SBATCH --error=log_compute_cl_%j.err
#SBATCH --output=log_compute_cl_%j.out
#SBATCH --ntasks-per-node=48
#SBATCH --array=0-3
##SBATCH --array=0-6

export OMP_NUM_THREADS=48
export PYTHONUNBUFFERED=1

#python compute_cl_noise_full.py LT$SLURM_ARRAY_TASK_ID
python compute_cl_noise_full.py ST$SLURM_ARRAY_TASK_ID
