import mapsims
import healpy as hp

content = "relative_hitmap"

for tube in mapsims.so_utils.tubes.keys():
    sim = mapsims.MapSim(channels=tube), other_components=mapsims.SONoiseSimulator())
    sim = mapsims.SONoiseSimulator(telescopes=[\"LA\",\"SA\"], nside=256, scanning_strategy=False, num=134,\n",
    "                       rolloff_ell=50, hitmap_version=\"v0.2\", full_covariance=False)"
    hp.write_map("outputs/hitmaps/" +f"simonsobs_{content}_{scanning_strategy}_{telescope}_nside{nside}.fits", noise.hitmap[telescope])
