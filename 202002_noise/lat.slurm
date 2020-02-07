#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims
#SBATCH --error=mapsims_%j.err
#SBATCH --output=mapsims_%j.out

NUM=0 
for TUBE in LT4 LT3 LT2 LT1 LT0 
do
    for NSPLITS in 1 4
    do
        mapsims_run --nsplits=$NSPLIT --channels $TUBE --num $NUM common.toml noise.toml
    done
done
