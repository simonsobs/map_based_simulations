#!/bin/bash
#SBATCH --partition=soap
#SBATCH --time={hours}:{minutes}:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48 
#SBATCH --job-name=mapsims_{simulation_type}_{nside}_{channels}
#SBATCH --error=mapsims_{simulation_type}_{nside}_{channels}_%j.err
#SBATCH --output=mapsims_{simulation_type}_{nside}_{channels}_%j.out

time mapsims_run --nside {nside} --channels {channels} ../common.toml ../{simulation_type}.toml
