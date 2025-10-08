# Draft Proposal: Next Map Domain Simulations

## Capabilities for Sky Modelling

### Available PySM3 Components and Models

**Dust**
- `d0`: Simple dust, fixed spectral index and temperature everywhere.
- `d1`: Planck Commander, single-component modified black body dust model.
- `d2`: Dust with spatially-varying emissivity, Gaussian random field variation.
- `d3`: Alternative spatially-varying dust emissivity, different Gaussian parameters.
- `d4`: Two-component dust model from Finkbeiner, Davis, Schlegel 1999 paper.
- `d5`: Dust model from Hensley and Draine 2017, advanced grain physics.
- `d6`: Analytic frequency decorrelation, spatial and line-of-sight variations.
- `d7`: Dust model with iron inclusions in grain composition, modified physics.
- `d8`: Dust model with fixed interstellar radiation field strength, simplified.
- `d9`: Like `d10` but fixed spectral index and temperature across the sky.
- `d10`: GNILC needlet-based dust template, reduced CIB contamination, high-res.
- `d11`: Stochastic small scales dust, generated on-the-fly, customizable seeds.
- `d12`: 3D six-layer dust model, MKD, Planck Sky Model based.

**Synchrotron**
- `s1`: Power law synchrotron, spatially-varying spectral index, Haslam/WMAP templates.
- `s2`: Synchrotron index steepens off Galactic plane, WMAP consistent model.
- `s3`: Curved index power law synchrotron, best-fit curvature amplitude applied.
- `s4`: Simplified synchrotron, fixed spectral index of -3.1 everywhere.
- `s5`: Power law synchrotron, logpoltens small scales, S-PASS rescaled index.
- `s6`: Stochastic small scales synchrotron, generated on-the-fly, customizable.
- `s7`: Curved index synchrotron, ARCADE patch, random small scale fluctuations.

**Anomalous Microwave Emission (AME)**
- `a1`: AME as sum of two spinning dust populations, Commander templates.
- `a2`: AME with 2% polarization fraction, simulated with dust polarization angles.

**Free-free**
- `f1`: Analytic free-free emission, Commander fit, degree-scale map at 30 GHz.

**CMB**
- `c1`: Lensed CMB realization computed using Taylens, CAMB input Cl’s.
- `c2`: Precomputed lensed CMB map, c1 model, nside 512 resolution.
- `c3`: Unlensed CMB map, WebSky 0.4 cosmological parameters, high-res.
- `c4`: Lensed CMB map, WebSky convergence map, nside 512/4096, high-res.

**CMB Dipole**
- `dip1`: Planck Public Release 4 Solar Dipole, amplitude and direction parameters.
- `dip2`: Solar dipole with frequency-dependent quadrupole correction, relativistic effects.

**CO Line Emission**
- `co1`: Galactic CO emission, first 3 rotational lines, Planck MILCA maps.
- `co2`: CO emission with 0.1% polarization, based on co1, added feature.
- `co3`: Mock CO clouds map, simulated 20 degrees off Galactic plane.

**Cosmic Infrared Background**
- `cib1`: Cosmic Infrared Background map, WebSky 0.4 simulation, interpolated frequencies.

**Sunyaev–Zeldovich Emission**
- `tsz1`: Thermal SZ emission from WebSky 0.4, nside 8192, high-res.
- `ksz1`: Kinetic SZ emission from WebSky 0.4, nside 4096, high-res.

**Radio Galaxies**
- `rg1`: Emission from radio galaxies, WebSky 0.4, not polarized, interpolated.
- `rg2`: Brightest radio galaxies, flux above 1 mJy, catalog-based, polarized.
- `rg3`: Background radio galaxies, flux below 1 mJy, pre-simulated, polarized.

**Planned addition:** Implement Half Dome extragalactic model (see [PySM issue #204](https://github.com/galsci/pysm/issues/204)), with SZ, CIB, Radio Galaxies and CMB components.

### Instrument characterization

## Bandpass
- Delta frequency (single frequency channel)
- Top-hat bandpass (uniform response over a frequency range)
- Realistic bandpass (measured or modeled instrument response)
- Generalization of bandpass sampling in PySM, this allows to generate different realistic for each wafer based on a reference bandpass ([issue #228](https://github.com/galsci/pysm/issues/228)).

## Beam
- Gaussian beam (simple analytic model)
- Beam window function in spherical harmonics domain (for more realistic instrument response)

## Proposed plan: Updated version of MBS 16

See the [Documentation of MBS-16](https://github.com/simonsobs/map_based_simulations/blob/main/mbs-s0016-20241111/README.md).
Our initial plan is to update MBS-16 with the latest instrument model and add Half-Dome extragalactic components (on top of Websky), if available.

### Sky modelling

For Galactic components the plan is to use the Low, Medium and High Complexity sky models, the same we used in MBS-16, they are described in the Documentation of MBS-16 and in the [PySM methods paper](https://iopscience.iop.org/article/10.3847/1538-4357/adf212). Moreover, for comparison with previous simulations, we plan on running also the `s1` and `d1` models.

For Extragalactic components the plan is to use Websky 0.4, including the Catalog-based radio galaxy components. If available, we plan to release also all the Half-Dome components, so they are available for comparison.

For CMB, we will use the Websky 0.4 lensed and un-lensed components and possibly Half-Dome. We will also simulate separately the CMB Solar Dipole with frequency-varying quadrupole `dip2`.

### Bandpass

Realistic wafer-by-wafer bandpasses generated using the Bandpass Sampler (which will be included in PySM) starting from a reference bandpass based on the latest instrument model. Need to decide how many wafers per band.

### Beam

The plan is to use Gaussian beams based on the most recently measured FWHM.

### Output maps

Output maps are both in CAR and HEALPix, with variable resolution by frequency,
using the same resolution used for real data.
Modelling is executed at twice the resolution and a minimum of NSIDE 2048,
in the final step, spherical harmonics are transformed to the target NSIDE or CAR resolution.
No intermediate maps are saved, only the final bandpass-integrated and beam-smoothed maps for each wafer.

Available maps:

* Map of each individual component for each wafer (stored on tape and available upon request)
* Combined maps of Low, Medium and High Complexity Galactic emission for each wafer
* Combined maps `s1d1` Galactic emission for each wafer
* Combined Websky CMB + CMB Dipole for each wafer
* If available combined Half-Dome CMB + CMB Dipole for each wafer
* Combined Websky Extragalactic components
* If available, combined Half-Dome Extragalactic components

### Additional Data products

* Instrument model with all parameters used
* Configuration files used to run `mapsims`

