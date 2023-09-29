'''
Plot output healpix maps and compare spectra to input TOD sims.
'''
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import os
import numpy as np

opj = os.path.join

mapdir = '/mnt/home/aduivenvoorden/project/so/20230524_sat_noise/v1'
outdir = opj(mapdir, 'out', 'run00')
imgdir = opj(mapdir, 'out/run00/img')
specdir = opj(outdir, 'spec')

freqs = ['f030', 'f040', 'f090', 'f150', 'f230', 'f290']
npol = 3
freq_pairs = [('f030', 'f040'), ('f090', 'f150'), ('f230', 'f290')]
weights = ['flat', 'ivar']
nsim = 300
pols = ['T', 'E', 'B']

for pair in freq_pairs:

    for sidx in range(1, 3):

        spectra_data = np.load(opj(specdir, f'spectra_{pair[0]}_{pair[1]}_set{sidx}_data.npy'))
        spectra_sims = np.load(opj(specdir, f'spectra_{pair[0]}_{pair[1]}_set{sidx}_sims.npy'))
        ells = np.load(opj(specdir, f'ells_{pair[0]}_{pair[1]}_set{sidx}_data.npy'))

        for widx, weight in enumerate(weights):
            for fidx1, freq1 in enumerate(pair):
                for fidx2, freq2 in enumerate(pair):

                    fig, axs = plt.subplots(ncols=3, nrows=3, dpi=300, constrained_layout=True, sharex=True)

                    for aidxs, ax in np.ndenumerate(axs):

                        for sim_idx in range(nsim):
                            label = 'draws' if sim_idx == 0 else None
                            axs[aidxs].plot(
                                ells, spectra_sims[widx,sim_idx,fidx1,fidx2,aidxs[0],aidxs[1]],
                                lw=0.5, color='firebrick', alpha=0.3, zorder=1, label=label)

                        sim_mean = np.mean(spectra_sims[widx,:,fidx1,fidx2,aidxs[0],aidxs[1]], axis=0)
                        sim_std = np.std(spectra_sims[widx,:,fidx1,fidx2,aidxs[0],aidxs[1]], axis=0)

                        axs[aidxs].fill_between(ells, sim_mean - sim_std, sim_mean + sim_std, color='black', alpha=1,
                                                label=r'draws $\pm 1 \sigma$')
                        axs[aidxs].plot(ells, spectra_data[widx,fidx1,fidx2,aidxs[0],aidxs[1]],
                                        lw=0.5, label='TOD sim')
                        axs[aidxs].text(0.8, 1.02, f'{pols[aidxs[0]]} x {pols[aidxs[1]]}',
                                        transform=axs[aidxs].transAxes)
                        
                        if aidxs[0] == aidxs[1] == 0:
                            axs[aidxs].set_yscale('log')
                            spec = spectra_data[widx,fidx1,fidx2,0,0]
                            smax = np.max(spec)
                            smin = np.min(spec[(ells > 50) & (ells < 250)])
                            axs[aidxs].set_ylim(1e-1 * smin, 3 * smax)
                            axs[aidxs].legend(frameon=False, loc='upper right')
                        else:
                            axs[aidxs].ticklabel_format(axis='y', style='sci', useOffset=False, scilimits=(0,0))
                        axs[aidxs].set_xlim(0, 250)

                    for pidx in range(3):
                        axs[pidx,0].set_ylabel(r'$C_{\ell}$ [$\mathrm{\mu K^2}$]')

                    for pidx in range(3):
                        axs[-1,pidx].set_xlabel(r'Multipole, $\ell$')

                    fig.suptitle(f'{freq1} x {freq2}, weighting : {weight}')
                    fig.savefig(opj(imgdir,
                            f'coadd_SAT_{freq1}_{freq2}_00{sidx}of002_spectra_{weight}_combined'))
                    plt.close(fig)
