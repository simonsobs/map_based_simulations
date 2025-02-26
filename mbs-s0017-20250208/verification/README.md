# Simulation verification

## Compare 353 GHz PySM to NPIPE Map

* [Run PySM with different bandpasses and compare](https://gist.github.com/zonca/c757aa0bff488231c95c1e6480172b02)

## CO Lines

[Verify CO Lines notebook](verify_CO.ipynb)

## Power spectra

All components except CO and Radio Galaxies,
the B Spectra of the CMB components are affected by high noise due to `ud_grade` performed in the on-the-fly run with PySM inside the notebook.
If the run is properly executed at Nside 4096, no artificial noise is visible anymore.

* [T](https://nbviewer.org/gist/zonca/a42e3aaea7a63914c338093a4062f828)
* [E](https://nbviewer.org/gist/zonca/1356c616351eee3b88f314731510e32a)
* [B](https://nbviewer.org/gist/zonca/dae682f67435780d747be59a4dfabf60)

# Visual inspection of maps

* [galactic_foregrounds_d1s1](https://nbviewer.org/gist/zonca/5636363d3451d8644ee6a244899e4364)
* [galactic_foregrounds_lowcomplexity](https://nbviewer.org/gist/zonca/df46ab650285e2f48a24a68199dabf9c)
* [galactic_foregrounds_mediumcomplexity](https://nbviewer.org/gist/zonca/5c2023d6891f8b10c1f8f16fbcad2234)
* [galactic_foregrounds_highcomplexity](https://nbviewer.org/gist/zonca/871f217a96e8558f41af2a063b6abc22)
