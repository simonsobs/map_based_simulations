NSIDE=512
for cfg in *$NSIDE*.cfg
do
    mapsims_run common.cfg $cfg
done
