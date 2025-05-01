#!/bin/bash
#SBATCH --partition=genx
#SBATCH --nodes=1
#SBATCH --time=4:00:00
#SBATCH --job-name=run_plot_cl
#SBATCH --error=../logs/run_plot_cl%j.out
#SBATCH --output=../logs/run_plot_cl%j.out
#SBATCH --cpus-per-task=48

export OMP_NUM_THREADS=48
export NUMBA_NUM_THREADS=$OMP_NUM_THREADS
export HDF5_USE_FILE_LOCKING=FALSE
export PYTHONUNBUFFERED=1

time bash run_plot_cl.sh
