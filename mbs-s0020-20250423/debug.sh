export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=12
cfg=ame_a1.toml
ch="B95"
ipython --pdb -- $(which mapsims_run) --verbose --channels=$ch common.toml $cfg
