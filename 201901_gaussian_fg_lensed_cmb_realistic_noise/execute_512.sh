
for SLURM_ARRAY_TASK_ID in $(seq 10 109)
do
    echo Simulation $SLURM_ARRAY_TASK_ID
    source output/512/noise/submit.slurm
    source output/512/cmb/submit.slurm
done
