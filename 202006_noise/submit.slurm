#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=1:00:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims
#SBATCH --error=mapsims_%j.err
#SBATCH --output=mapsims_%j.out
#SBATCH --ntasks-per-node=48
#SBATCH --array=0-6

export OMP_NUM_THREADS=48
export PYTHONUNBUFFERED=1

NUM=0
TUBE=LT$SLURM_ARRAY_TASK_ID
for NSPLITS in 1 4
do
    mapsims_run --nsplits=$NSPLITS --channels="tube:$TUBE" --num=$NUM common.toml noise.toml
done
