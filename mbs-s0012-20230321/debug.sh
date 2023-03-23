#for cfg in cib.toml # ksz.toml tsz.toml radio.toml cmb.toml cmb_unlensed.toml
# for cfg in cmb.toml cmb_unlensed.toml
export PYTHONUNBUFFERED=1
#export OMP_PROC_BIND=true
#export OMP_PLACES=threads
#export OMP_NUM_THREADS=68
#export HDF5_USE_FILE_LOCKING=FALSE
cfg=dust.toml
ipython --pdb -- $(which mapsims_run) --verbose --channels='LAT_f290' common.toml $cfg
