export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=48
cfg=radio_rg2.toml
ch=SAT_f030_w1
ipython --pdb -- $(which mapsims_run) --verbose --channels=$ch common.toml $cfg
