#!/bin/bash
#SBATCH --qos=regular
#SBATCH --time=3:00:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims
#SBATCH --constraint=haswell
#SBATCH --mail-user
#SBATCH --error=mapsims_%j.err
#SBATCH --output=mapsims_%j.out

time python run.py
