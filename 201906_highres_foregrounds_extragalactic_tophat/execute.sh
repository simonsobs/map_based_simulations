NSIDE=512
for cfg in *$NSIDE*.toml
do
    mapsims_run --nside=$NSIDE common.toml $cfg
done
