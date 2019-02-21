#!/bin/bash
#SBATCH --qos=regular
#SBATCH --time={hours}:{minutes}:00
#SBATCH --nodes=1
#SBATCH --job-name=mapsims_{simulation_type}_{nside}
#SBATCH --constraint=haswell
#SBATCH --mail-user
#SBATCH --error=mapsims_{simulation_type}_{nside}_%j.err
#SBATCH --output=mapsims_{simulation_type}_{nside}_%j.out
#SBATCH --array={first_sim_id}-{last_sim_id}

NUM=$(printf "%04d" $SLURM_ARRAY_TASK_ID)
sim={simulation_type}
NSIDE={nside}
CHANNELS={channels}
template_config_file=common.cfg
output_folder="output/$NSIDE/$sim/$NUM"
mkdir -p $output_folder
config_file="$output_folder/common.cfg"
sed "s/0000/$NUM/" $template_config_file | sed "s/512/$NSIDE/" | sed "s/all/$CHANNELS/" > $config_file
echo "MAPSIMS RUN: $NSIDE $sim $NUM"
sim+='.cfg'
time mapsims_run $config_file $sim
