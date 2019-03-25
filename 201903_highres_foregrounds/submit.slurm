#!/bin/bash
#SBATCH --qos=regular
#SBATCH --time={hours}:{minutes}:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims_{simulation_type}_{nside}
#SBATCH --constraint=haswell
#SBATCH --mail-user
#SBATCH --error=mapsims_{simulation_type}_{nside}_%j.err
#SBATCH --output=mapsims_{simulation_type}_{nside}_%j.out

NUM=0000
sim={simulation_type}
NSIDE={nside}
CHANNELS={channels}
template_config_file=common_{nside}.cfg
output_folder="output/$NSIDE/$sim/$NUM"
mkdir -p $output_folder
config_file="$output_folder/common.cfg"
cp $template_config_file $config_file
echo "MAPSIMS RUN: $NSIDE $sim $NUM"
sim+="_{nside}.cfg"
time mapsims_run $config_file $sim
