import os

import numpy as np
from mpi4py import MPI
from pixell import enmap, curvedsky, mpi as p_mpi
from mnms import utils

opj = os.path.join
comm = MPI.COMM_WORLD

imapdir = '/mnt/home/aduivenvoorden/project/so/20240504_mss0002_lat/renamed'
simdir = '/mnt/home/aduivenvoorden/project/actpol/maps/mnms/sims'
maskdir = '/mnt/home/aduivenvoorden/project/so/20240504_mss0002_lat/masks'
imgdir = '/mnt/home/aduivenvoorden/project/so/20240504_mss0002_lat/compared'

os.makedirs(imgdir, exist_ok=True)

freqs = [('f030', 'f040'), ('f090', 'f150'), ('f230', 'f290')]
splits = ['split0']

lmax = 5400
ainfo = curvedsky.alm_info(lmax)

npol = 3
nell = lmax + 1
nsim = 300

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

for freq_pair in freqs:

    print(comm.rank, freq_pair)
    
    if freq_pair == ('f030', 'f040'):
        qstr = 'lf'
    elif freq_pair == ('f090', 'f150'):
        qstr = 'mf'
    else:
        qstr = 'uhf'

    mask = enmap.read_map(
        opj(maskdir, f'LAT_{freq_pair[0]}_{freq_pair[1]}_mask_est.fits'))

    shape_dg, wcs_dg = enmap.read_map_geometry(
        opj(simdir, f'so_lat_mbs_mss0002_fdw_{qstr}_{qstr}_{freq_pair[0]}' + \
            f'_{qstr}_{freq_pair[1]}_lmax5400_4way_set0_noise_sim_map0000.fits'))

    mask_dg = utils.fourier_resample(mask, shape=shape_dg, wcs=wcs_dg)
    
    for sidx, split in enumerate(splits):

        spectra = np.zeros((nsim, 2, npol, 2, npol, nell))

        alms = np.zeros((2, npol, ainfo.nelem), dtype=np.complex128)

        if comm.rank == 0:

            spectra_data = np.zeros((2, npol, 2, npol, nell))        
            
            for fidx, freq in enumerate(freq_pair):

                imap = enmap.read_map(
                    opj(imapdir, f'sobs_RC1.r01_LAT_mission_{freq}_4way_{split}_noise_map_car.fits'))

                alms[fidx] = curvedsky.map2alm(imap * mask, ainfo=ainfo)

            for fidx1 in range(2):
                for fidx2 in range(fidx1, 2):
                    spectra_data[fidx1,:,fidx2,:,:] = ainfo.alm2cl(
                        alms[fidx1][:,None,:], alms[fidx2][None,:,:])
                    
            np.save(opj(imgdir, f'spectra_data_{qstr}'), spectra_data)                            

        comm.Barrier()
            
        for didx in range(comm.rank,nsim,comm.size):

            print(comm.rank, didx)

            sim = enmap.read_map(
                opj(simdir, f'so_lat_mbs_mss0002_fdw_{qstr}_{qstr}_{freq_pair[0]}' + \
                    '_{qstr}_{freq_pair[1]}_lmax5400_4way_set{sidx}_noise_sim_map{didx:04d}.fits'))
                    
            for fidx, freq in enumerate(freq_pair):

                alms[fidx] = curvedsky.map2alm(sim[fidx,0] * mask_dg, ainfo=ainfo)

            for fidx1 in range(2):
                for fidx2 in range(fidx1, 2):
                    spectra[didx,fidx1,:,fidx2,:,:] = ainfo.alm2cl(
                        alms[fidx1][:,None,:], alms[fidx2][None,:,:])

        spectra = reduce_array(spectra, comm, op=None, root=0)

        if comm.rank == 0:
            np.save(opj(imgdir, f'spectra_sims_{qstr}'), spectra)
