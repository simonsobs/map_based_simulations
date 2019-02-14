#!/bin/bash
#SBATCH --qos=regular
#SBATCH --time=3:30:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims
#SBATCH --constraint=haswell
#SBATCH --mail-user
#SBATCH --error=mapsims_%j.err
#SBATCH --output=mapsims_%j.out

NUM="0000"
sim=foreground
nside=512
template_config_file=common.cfg
output_folder="output/$nside/$sim/$NUM"
mkdir -p $output_folder
config_file="$output_folder/common.cfg"
sed "s/0000/${NUM}/" $template_config_file > $config_file
time mapsims_run $config_file ${sim}.cfg
