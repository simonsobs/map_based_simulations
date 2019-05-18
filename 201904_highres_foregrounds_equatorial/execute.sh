NSIDE=512
for cfg in *$NSIDE*.toml
do
    mapsims_run common.toml $cfg
done
