#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=10:00:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims
#SBATCH --error=mapsims_%j.err
#SBATCH --output=mapsims_%j.out
#SBATCH --ntasks-per-node=48

export OMP_NUM_THREADS=48
export PYTHONUNBUFFERED=1

NUM=0 
for TUBE in ST0 ST1 ST2 ST3 LT7 LT6 LT5 LT4 LT3 LT2 LT1 LT0
do
    for NSPLITS in 1 4
    do
        mapsims_run --nsplits=$NSPLITS --channels=$TUBE --num=$NUM common.toml noise.toml
    done
done
