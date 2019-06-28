import mapsims
import healpy as hp

content = "relative_hitmap"

for nside in [512, 4096]:
    for scanning_strategy in ["classical", "opportunistic"]:
        noise = mapsims.SONoiseSimulator(nside=nside, scanning_strategy=scanning_strategy)
        for telescope in ["SA", "LA"]:
            hp.write_map("/home/zonca/comet/simonsobs/hitmaps/" +f"simonsobs_{content}_{scanning_strategy}_{telescope}_nside{nside}.fits", noise.hitmap[telescope])
