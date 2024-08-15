import os
import time

import numpy as np
import matplotlib.pyplot as plt

opj = os.path.join

imgdir = '/mnt/home/aduivenvoorden/project/so/20240504_mss0002_lat/compared'

freqs = [('f030', 'f040'), ('f090', 'f150'), ('f230', 'f290')]
splits = ['split0']

lmax = 5400

npol = 3
nell = lmax + 1
nsim = 300
pols = ['T', 'E', 'B']

ells = np.arange(nell)

for pair in freqs:
    
    if pair == ('f030', 'f040'):
        qstr = 'lf'
    elif pair == ('f090', 'f150'):
        qstr = 'mf'
    else:
        qstr = 'uhf'
    
    for sidx, split in enumerate(splits):

        spectra_data = np.load(opj(imgdir, f'spectra_data_{qstr}.npy'))
        spectra_sims = np.load(opj(imgdir, f'spectra_sims_{qstr}.npy'))
        
        for fidx1, freq1 in enumerate(pair):
            for fidx2, freq2 in enumerate(pair):

                if fidx2 < fidx1:
                    continue
                
                fig, axs = plt.subplots(ncols=3, nrows=3, dpi=300, constrained_layout=True, sharex=True,
                                        figsize=(10, 10))

                for aidxs, ax in np.ndenumerate(axs):

                    for sim_idx in range(nsim):
                        label = 'draws' if sim_idx == 0 else None
                        axs[aidxs].plot(
                            ells, spectra_sims[sim_idx,fidx1,aidxs[0],fidx2,aidxs[1]],
                            lw=0.5, color='firebrick', alpha=0.3, zorder=1, label=label)

                    sim_mean = np.mean(spectra_sims[:,fidx1,aidxs[0],fidx2,aidxs[1]], axis=0)
                    sim_std = np.std(spectra_sims[:,fidx1,aidxs[0],fidx2,aidxs[1]], axis=0)

                    axs[aidxs].fill_between(ells, sim_mean - sim_std, sim_mean + sim_std, color='black', alpha=1,
                                            label=r'draws $\pm 1 \sigma$')
                    axs[aidxs].plot(ells, spectra_data[fidx1,aidxs[0],fidx2,aidxs[1]],
                                    lw=0.5, label='TOD sim')
                    axs[aidxs].text(0.8, 1.02, f'{pols[aidxs[0]]} x {pols[aidxs[1]]}',
                                    transform=axs[aidxs].transAxes)

                    if aidxs[0] == aidxs[1]:
                        if fidx1 == fidx2:
                            axs[aidxs].set_yscale('log')
                        #else:
                        #    axs[aidxs].set_yscale('symlog', linthresh=1e-4)
                        spec = spectra_data[fidx1,0,fidx2,0]
                        #smax = np.max(spec)
                        #smin = np.min(spec[(ells > 50) & (ells < 250)])
                        #axs[aidxs].set_ylim(1e-1 * smin, 3 * smax)
                        axs[aidxs].legend(frameon=False, loc='upper right')
                    else:
                        axs[aidxs].ticklabel_format(axis='y', style='sci', useOffset=False, scilimits=(0,0))
                    axs[aidxs].set_xlim(1, 5000)
                    axs[aidxs].set_xscale('log')

                for pidx in range(3):
                    axs[pidx,0].set_ylabel(r'$C_{\ell}$ [$\mathrm{\mu K^2}$]')

                for pidx in range(3):
                    axs[-1,pidx].set_xlabel(r'Multipole, $\ell$')

                fig.suptitle(f'{freq1} x {freq2}')
                fig.savefig(opj(imgdir, f'so_lat_mbs_mss0002_fdw_{freq1}_{freq2}_set{sidx}_spectra'))
                                
                plt.close(fig)
        
