from mnms import noise_models as nm

config_name = 'so_lat_mbs_mss0002'
noise_model_name = 'fdw_mf' # For LF use "fdw_lf", for MF use "fdw_mf" and for UHF use "fdw_uhf"
qids = ['mfa', 'mfb'] # Simulate f090 and f150 jointly.
lmax = 5400

model = nm.BaseNoiseModel.from_config(config_name, noise_model_name, qids)

# Draw the simulation. This can be repeated for different sim_idx values.
sim_idx = 300
split_idx = 0 # Pick 0, 1, 2 or 3.
sim = model.get_sim(split_idx, sim_idx, lmax, alm=False, write=False, verbose=True)
