'''
Plot output healpix maps and compare spectra to input TOD sims.
'''
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import os
import numpy as np

import healpy as hp
import pymaster as nmt
from pixell import enmap, sharp, curvedsky, reproject, enplot, mpi as p_mpi
from optweight import mat_utils

from mpi4py import MPI
comm = MPI.COMM_WORLD

opj = os.path.join

mapdir = '/mnt/home/aduivenvoorden/project/so/20230524_sat_noise/v1'
cardir = '/mnt/home/aduivenvoorden/project/so/20230524_sat_noise/v1/car'
outdir = opj(mapdir, 'out', 'run00')
maskdir = opj(cardir, 'masks')
imgdir = opj(mapdir, 'out/run00/img')
specdir = opj(outdir, 'spec')

os.makedirs(imgdir, exist_ok=True)
os.makedirs(specdir, exist_ok=True)

def numpy_to_mpi_type(dtype):
    '''
    Convert numpy dtype to MPI data_type.

    Paramters
    ---------
    dtype : dtype
        Numpy dtype

    Returns
    -------
    data_type : mpi4py.MPI.Datatype
        Corresponding MPI data type.
    '''

    # Will crash if no MPI, but OK, this function should not have been called.
    from mpi4py import MPI
    # Could also used mpi.util.dtlib. But was only added in mpi4py 3.1.0.
    return MPI._typedict[np.dtype(dtype).char]

def bcast_array_meta(arr, comm, root=0):
    '''
    Broadcast shape and dtype of array.

    Parameters
    ----------
    arr : array, None
        Array on root.
    comm : MPI communicator
    root : int, optional
        Broadcast info from this rank.

    Returns
    -------
    shape : tuple
    dtype : type
    '''

    if isinstance(comm, p_mpi.FakeCommunicator) or comm.Get_size() == 1:
        return arr.shape, arr.dtype

    if comm.Get_rank() == root:
        shape = arr.shape
        dtype = arr.dtype
    else:
        shape, dtype = None, None

    shape = comm.bcast(shape, root=root)
    dtype = comm.bcast(dtype, root=root)

    return shape, dtype

def bcast_array(arr, comm, root=0):
    '''
    Broadcast array.

    Parameters
    ----------
    arr : array
        Array on root.
    comm : MPI communicator
    root : int, optional
        Broadcast array from this rank.

    Returns
    -------
    arr_out : array
        Broadcasted array on all ranks.
    '''

    if isinstance(comm, p_mpi.FakeCommunicator) or comm.Get_size() == 1:
        return arr

    shape, dtype = bcast_array_meta(arr, comm, root=root)

    if comm.Get_rank() != root:
        arr = np.zeros(shape, dtype=dtype)

    mpi_type = numpy_to_mpi_type(arr.dtype)
    comm.Bcast([arr, mpi_type], root=root)

    return arr

def reduce_array(arr, comm, op=None, root=0):
    '''
    Reduce numpy array to root.

    Parameters
    ----------
    arr : array
    comm : MPI communicator
    op : mpi4py.MPI.Op object, optional
        Operation during reduce, defaults to SUM.
    root : int, optional
        Reduce array to this rank.

    Returns
    -------
    arr_out : array, None
        Reduced array on root, None on other ranks.
    '''

    if isinstance(comm, p_mpi.FakeCommunicator) or comm.Get_size() == 1:
        return arr

    if comm.Get_rank() == root:
        arr_out = np.zeros_like(arr)
    else:
        arr_out = None

    if op is not None:
        comm.Reduce(arr, arr_out, op=op, root=root)
    else:
        comm.Reduce(arr, arr_out, root=root)

    return arr_out

freqs = ['f030', 'f040', 'f090', 'f150', 'f230', 'f290']
npol = 3
freq_pairs = [('f030', 'f040'), ('f090', 'f150'), ('f230', 'f290')]

def compute_master(f_a, f_b, wsp):
    '''
    Compute MASTER spectrum.

    Parameters
    ----------
    f_a : NmtField
        First field.
    f_c : NmtField
        Second field.
    wsp : NmtWorkspace
        Workspace containing coupling matrix.

    Returns
    -------
    cl_decoupled : array
        Decoupled C_ells, shape varies based on spin.
    '''

    cl_coupled = nmt.compute_coupled_cell(f_a, f_b)
    cl_decoupled = wsp.decouple_cell(cl_coupled)

    return cl_decoupled

for pair in freq_pairs:

    if comm.rank == 0:
        mask_obs = hp.read_map(opj(maskdir, f'coadd_SAT_{pair[0]}_{pair[1]}_mask_obs_hp.fits'))
        nside = hp.npix2nside(mask_obs.shape[-1])

        # Reproject mask_est.
        mask_est = enmap.read_map(opj(maskdir, f'coadd_SAT_{pair[0]}_{pair[1]}_mask_est.fits'))
        shape = mask_est.shape
        wcs =  mask_est.wcs
        mask_est = reproject.map2healpix(mask_est, nside=nside, extensive=False,
                                        method='spline', order=1, spin=0)
        meta = [nside, shape, wcs]
    else:
        mask_est, mask_obs = None, None
        meta = None

    mask_obs = bcast_array(mask_obs, comm)
    mask_est = bcast_array(mask_est, comm)
    meta = comm.bcast(meta, root=0)
    nside, shape, wcs = meta

    for sidx in range(1, 3):

        nmt_fields = {}
        masks = {}
        vmin_dict = {}
        vmax_dict = {}

        for freq in pair:

            nmt_fields[freq] = {}

            if comm.rank == 0:
                imap_data = hp.read_map(
                    opj(mapdir, f'coadd_SAT_{freq}_00{sidx}of002_map.fits'),
                    field=None)
                imap_data[imap_data == hp.UNSEEN] = 0

                ivar_data = hp.read_map(
                    opj(mapdir, f'coadd_SAT_{freq}_00{sidx}of002_invcov.fits'),
                    field=0)
                ivar_data[ivar_data == hp.UNSEEN] = 0
            else:
                imap_data, ivar_data = None, None
            imap_data = bcast_array(imap_data, comm)
            ivar_data = bcast_array(ivar_data, comm)

            imap_data *= 1e6
            ivar_data *= 1e-12

            # Plot data maps.
            if freq in ('f030', 'f040'):
                font_size = 20
                downgrade = None
            elif freq in ('f090', 'f150'):
                font_size = 60
                downgrade = 2
            else:
                font_size = 80
                downgrade = 6

            # For visual comparison, reproject map using nearest-neighbor.
            tmin, tmax = (np.quantile(imap_data[0], 0.01), np.quantile(imap_data[0], 0.99))
            pmin, pmax = (np.quantile(imap_data[1], 0.01), np.quantile(imap_data[1], 0.99))
            vmin = [tmin, pmin, pmin]
            vmax = [tmax, pmax, pmax]
            vmin_dict[freq] = vmin
            vmax_dict[freq] = vmax

            if comm.rank == 0:
                # Note, we apply mask_obs.
                omap_spline = reproject.healpix2map(
                    imap_data * mask_obs, shape=shape, wcs=wcs, extensive=False,
                    method='spline', order=0)
                for pidx in range(npol):
                    plot = enplot.plot(omap_spline[pidx], colorbar=True, ticks=30,
                                       min=vmin[pidx], max=vmax[pidx],
                                       font_size=font_size)
                    enplot.write(opj(imgdir, f'coadd_SAT_{freq}_00{sidx}of002_map_spline_{pidx}'), plot)

            # Init namaster fields.
            bins = nmt.NmtBin.from_nside_linear(nside, 10)
            ells = bins.get_effective_ells()
            lmax = int(ells[-1] + 100)

            for weight in ['flat', 'ivar']:

                nmt_fields[freq][weight] = {}

                mask_eff = np.zeros((1, mask_est.shape[-1]), dtype=ivar_data.dtype)
                if weight == 'ivar':
                    mask_eff[0] = ivar_data / ivar_data.max() * mask_est
                else:
                    mask_eff[0] = mask_est

                masks[weight] = mask_eff

                f0 = nmt.NmtField(mask_eff[0], [imap_data[0]], lmax_sht=lmax)
                f2 = nmt.NmtField(mask_eff[0] , [imap_data[1], imap_data[2]], lmax_sht=lmax)

                nmt_fields[freq][weight]['f0'] = f0
                nmt_fields[freq][weight]['f2'] = f2

        if comm.rank == 0:
            np.save(opj(specdir, f'ells_{pair[0]}_{pair[1]}_set{sidx}_data'), ells)
                
        workspaces = {}
        weights = ['flat', 'ivar']

        for weight in weights:
            for freq1 in pair:
                for freq2 in pair:
                    for spin1 in [0, 2]:
                        for spin2 in [0, 2]:

                            if comm.rank == 0:
                                print(freq1, freq1, spin1, spin2)

                            wsp = nmt.NmtWorkspace()
                            f_a = nmt_fields[freq1][weight][f'f{spin1}']
                            f_b = nmt_fields[freq1][weight][f'f{spin2}']

                            wsp.compute_coupling_matrix(f_a, f_b, bins)

                            workspaces[f'{weight}_{freq1}_{freq2}_{spin1}_{spin2}'] = wsp

        spectra_data = np.zeros((len(weights), 2, 2, 3, 3, ells.size))

        for widx, weight in enumerate(weights):
            for fidx1, freq1 in enumerate(pair):

                f_a_0 = nmt_fields[freq1][weight]['f0']
                f_a_2 = nmt_fields[freq1][weight]['f2']

                for fidx2, freq2 in enumerate(pair):

                    if comm.rank == 0:
                        print(widx, fidx1, fidx2)

                    f_b_0 = nmt_fields[freq2][weight]['f0']
                    f_b_2 = nmt_fields[freq2][weight]['f2']

                    cl_00 = compute_master(
                        f_a_0, f_b_0, workspaces[f'{weight}_{freq1}_{freq2}_0_0'])
                    cl_02 = compute_master(
                        f_a_0, f_b_2, workspaces[f'{weight}_{freq1}_{freq2}_0_2'])
                    cl_20 = compute_master(
                        f_a_2, f_b_0, workspaces[f'{weight}_{freq1}_{freq2}_2_0'])
                    cl_22 = compute_master(
                        f_a_2, f_b_2, workspaces[f'{weight}_{freq1}_{freq2}_2_2'])

                    spectra_data[widx,fidx1,fidx2,0,0] =  cl_00[0]
                    spectra_data[widx,fidx1,fidx2,0,1] =  cl_02[0]
                    spectra_data[widx,fidx1,fidx2,0,2] =  cl_02[1]
                    spectra_data[widx,fidx1,fidx2,1,0] =  cl_20[0]
                    spectra_data[widx,fidx1,fidx2,1,1] =  cl_22[0]
                    spectra_data[widx,fidx1,fidx2,1,2] =  cl_22[1]
                    spectra_data[widx,fidx1,fidx2,2,0] =  cl_20[1]
                    spectra_data[widx,fidx1,fidx2,2,1] =  cl_22[2]
                    spectra_data[widx,fidx1,fidx2,2,2] =  cl_22[3]

        if comm.rank == 0:
            np.save(opj(specdir, f'spectra_{pair[0]}_{pair[1]}_set{sidx}_data'), spectra_data)

            for widx, weight in enumerate(weights):
                for fidx1, freq1 in enumerate(pair):
                    for fidx2, freq2 in enumerate(pair):

                        fig, axs = plt.subplots(ncols=3, nrows=3, dpi=300, constrained_layout=True)

                        for aidxs, ax in np.ndenumerate(axs):

                            axs[aidxs].plot(ells, spectra_data[widx,fidx1,fidx2,aidxs[0],aidxs[1]],
                                            lw=0.5)

                            if aidxs[0] == aidxs[1]:
                                axs[aidxs].set_yscale('linear')
                            # This is a fun bug in matplotlib.
                            axs[aidxs].set_xscale('linear')
                            axs[aidxs].set_xscale('log')
                            axs[aidxs].set_xscale('linear')
                            axs[aidxs].set_xlim(0, 200)
                        fig.savefig(opj(imgdir,
                                f'coadd_SAT_{freq1}_{freq2}_00{sidx}of002_spectra_{weight}_linear'))
                        plt.close(fig)

        # Now, compute the same for the sims.
        nsim = 300
        spectra_sims = np.zeros((len(weights), nsim, 2, 2, 3, 3, ells.size))

        nmt_fields = {}

        for sim_idx in range(comm.rank, nsim, comm.size):

            for freq in pair:
                print(f'{freq}, sim {sim_idx}')
                nmt_fields[freq] = {}

                imap_sim = hp.read_map(
                    opj(outdir,
                        f'so_sat_v1_f1_tile_{freq}_2way_set{sidx-1}_noise_sim_map{sim_idx:04d}.fits'),
                    field=None)

                imap_sim *= 1e6

                # Plot sim.
                if freq in ('f030', 'f040'):
                    font_size = 20
                    downgrade = None
                elif freq in ('f090', 'f150'):
                    font_size = 60
                    downgrade = 2
                else:
                    font_size = 80
                    downgrade = 6

                if sim_idx == 0:
                    # For visual comparison, reproject map using nearest-neighbor.
                    vmin = vmin_dict[freq]
                    vmax = vmax_dict[freq]

                    omap_spline = reproject.healpix2map(imap_sim, shape=shape, wcs=wcs, extensive=False,
                                                        method='spline', order=0)
                    for pidx in range(npol):

                        plot = enplot.plot(omap_spline[pidx], colorbar=True, ticks=30,
                                           min=vmin[pidx], max=vmax[pidx],
                                           font_size=font_size)
                        enplot.write(
                            opj(imgdir,
                        f'so_sat_v1_f1_tile_{freq}_2way_set{sidx-1}_noise_sim_map{sim_idx:04d}_{pidx}'),
                            plot)

                for weight in ['flat', 'ivar']:

                    nmt_fields[freq][weight] = {}

                    f0 = nmt.NmtField(masks[weight][0], [imap_sim[0]], lmax_sht=lmax)
                    f2 = nmt.NmtField(masks[weight][0] , [imap_sim[1], imap_sim[2]], lmax_sht=lmax)

                    nmt_fields[freq][weight]['f0'] = f0
                    nmt_fields[freq][weight]['f2'] = f2

            for widx, weight in enumerate(weights):
                for fidx1, freq1 in enumerate(pair):

                    f_a_0 = nmt_fields[freq1][weight]['f0']
                    f_a_2 = nmt_fields[freq1][weight]['f2']

                    for fidx2, freq2 in enumerate(pair):

                        f_b_0 = nmt_fields[freq2][weight]['f0']
                        f_b_2 = nmt_fields[freq2][weight]['f2']

                        cl_00 = compute_master(
                            f_a_0, f_b_0, workspaces[f'{weight}_{freq1}_{freq2}_0_0'])
                        cl_02 = compute_master(
                            f_a_0, f_b_2, workspaces[f'{weight}_{freq1}_{freq2}_0_2'])
                        cl_20 = compute_master(
                            f_a_2, f_b_0, workspaces[f'{weight}_{freq1}_{freq2}_2_0'])
                        cl_22 = compute_master(
                            f_a_2, f_b_2, workspaces[f'{weight}_{freq1}_{freq2}_2_2'])

                        spectra_sims[widx,sim_idx,fidx1,fidx2,0,0] =  cl_00[0]
                        spectra_sims[widx,sim_idx,fidx1,fidx2,0,1] =  cl_02[0]
                        spectra_sims[widx,sim_idx,fidx1,fidx2,0,2] =  cl_02[1]
                        spectra_sims[widx,sim_idx,fidx1,fidx2,1,0] =  cl_20[0]
                        spectra_sims[widx,sim_idx,fidx1,fidx2,1,1] =  cl_22[0]
                        spectra_sims[widx,sim_idx,fidx1,fidx2,1,2] =  cl_22[1]
                        spectra_sims[widx,sim_idx,fidx1,fidx2,2,0] =  cl_20[1]
                        spectra_sims[widx,sim_idx,fidx1,fidx2,2,1] =  cl_22[2]
                        spectra_sims[widx,sim_idx,fidx1,fidx2,2,2] =  cl_22[3]

        spectra_sims = reduce_array(spectra_sims, comm, op=None, root=0)
        
        if comm.rank == 0:
            np.save(opj(specdir, f'spectra_{pair[0]}_{pair[1]}_set{sidx}_sims'), spectra_sims)

            for widx, weight in enumerate(weights):
                for fidx1, freq1 in enumerate(pair):
                    for fidx2, freq2 in enumerate(pair):

                        fig, axs = plt.subplots(ncols=3, nrows=3, dpi=300, constrained_layout=True)

                        for aidxs, ax in np.ndenumerate(axs):

                            for sim_idx in range(nsim):
                                axs[aidxs].plot(
                                    ells, spectra_sims[widx,sim_idx,fidx1,fidx2,aidxs[0],aidxs[1]],
                                    lw=0.5, color='black', alpha=0.3)
                            axs[aidxs].plot(ells, spectra_data[widx,fidx1,fidx2,aidxs[0],aidxs[1]],
                                            lw=0.5)

                            if aidxs[0] == aidxs[1]:
                                axs[aidxs].set_yscale('linear')
                            # This is a fun bug in matplotlib.
                            axs[aidxs].set_xscale('linear')
                            axs[aidxs].set_xscale('log')
                            axs[aidxs].set_xscale('linear')
                            axs[aidxs].set_xlim(0, 200)
                        fig.savefig(opj(imgdir,
                                f'coadd_SAT_{freq1}_{freq2}_00{sidx}of002_spectra_{weight}_sim_linear'))
                        plt.close(fig)
