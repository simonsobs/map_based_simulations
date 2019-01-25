import numpy as np
import healpy as hp

from astropy.utils import data

import mapsims
import so_pysm_models



simulator = mapsims.from_config(
    "example_config.cfg"
)
output_map = simulator.execute(write_outputs=False)[simulator.channels[0]]

expected_map = hp.read_map(
    data.get_pkg_data_filename("tests/data/example_run.fits.gz", package="mapsims"), (0, 1, 2)
)
np.testing.assert_allclose(output_map, expected_map)
