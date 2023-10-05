export OMP_NUM_THREADS=48
export PYTHONUNBUFFERED=1

NUM=0
for I_TUBE in 0 1 2 3
do
    TUBE=ST$I_TUBE
    for NSPLITS in 1 4
    do
        mapsims_run --nsplits=$NSPLITS --channels="tube:$TUBE" --num=$NUM common.toml noise.toml
    done
done
