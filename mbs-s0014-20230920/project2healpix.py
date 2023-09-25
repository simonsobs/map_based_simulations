'''
Reproject the CAR sims to HEALPix.
'''
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import os
import numpy as np
import argparse
import glob

import healpy as hp
from pixell import enmap, enplot, reproject, curvedsky, mpi as p_mpi
from optweight import mat_utils, map_utils
from mnms import noise_models as nm

opj = os.path.join

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

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--config-name', type=str, required=True,
                    help='Name of model config file from which to load parameters')
parser.add_argument('--noise-model-name', dest='noise_model_name', type=str, required=True,
                    help='Name of model within config file from which to load parameters')
parser.add_argument('--qid', dest='qid', nargs='+', type=str, required=True,
                    help='list of array "qids"')
parser.add_argument('--lmax', dest='lmax', type=int, required=True,
                    help='Bandlimit of covariance matrix.')
parser.add_argument('--maps', dest='maps', nargs='+', type=str, default=None,
                    help='simulate exactly these map_ids')
parser.add_argument('--maps-start', dest='maps_start', type=int, default=None,
                    help='like --maps, except iterate starting at this map_id')
parser.add_argument('--maps-end', dest='maps_end', type=int, default=None,
                    help='like --maps, except end iteration with this map_id')
parser.add_argument('--maps-step', dest='maps_step', type=int, default=1,
                    help='like --maps, except step iteration over map_ids by '
                    'this number')
parser.add_argument('--mask-obs', type=str, required=True,
                    help='HEALPix map with mask_obs. Also determines output nside.')
parser.add_argument('--odir', type=str, required=True,
                    help='Output directory')
parser.add_argument('--split-idx', type=int, required=True,
                    help='Split index')
parser.add_argument('--oname-template', type=str, required=True,
                    help='A string for the output name with entries for freq, sidx and '
                    'sim_num, e.g. '
                    'so_sat_v1_f1_tile_{freq}_2way_set{sidx}_noise_sim_map{sim_num:04d}.fits')
parser.add_argument('--no-mpi', action='store_true',
                    help='Do not use MPI to compute models in parallel')
args = parser.parse_args()

if args.maps is not None:
    assert args.maps_start is None and args.maps_end is None
    maps = np.atleast_1d(args.maps).astype(int)
else:
    assert args.maps_start is not None and args.maps_end is not None
    maps = np.arange(args.maps_start, args.maps_end+args.maps_step, args.maps_step)
assert np.all(maps >= 0)

if args.no_mpi:
    comm = p_mpi.FakeCommunicator()
else:
    # Could add try statement, but better to crash if MPI cannot be imported.
    from mpi4py import MPI
    comm = MPI.COMM_WORLD

if comm.rank == 0:
    os.makedirs(args.odir, exist_ok=True)
comm.Barrier()
    
NM = nm.BaseNoiseModel.from_config(args.config_name, args.noise_model_name, *args.qid)

# Load and reproject ivar on root.
if comm.rank == 0:

    # First read expected geometry.
    shape, wcs = enmap.read_map_geometry(
        NM._data_model.get_map_fn(args.qid[0], split_num=args.split_idx, maptag='ivar'))
    ivar = enmap.zeros((len(args.qid),) + shape[-2:], wcs=wcs, dtype=np.float32)
    
    for qidx, qid in enumerate(args.qid):
        ivar[qidx] = enmap.read_map(
            NM._data_model.get_map_fn(qid, split_num=args.split_idx, maptag='ivar'))

    # This is ugly, but needed to compensate for upgraded ivars.
    ivar = ivar.downgrade(2)
    
    mask_obs = hp.read_map(args.mask_obs)
    nside = hp.npix2nside(mask_obs.shape[-1])
    ivar_hp = reproject.map2healpix(ivar, nside=nside, extensive=False,
                                    method='spline', order=1, spin=0)
else:
    ivar, ivar_hp, mask_obs = None, None, None
if not args.no_mpi:
    ivar = bcast_array(ivar, comm)
    ivar_hp = bcast_array(ivar_hp, comm)
    mask_obs = bcast_array(mask_obs, comm)

nside = hp.npix2nside(mask_obs.shape[-1])
# Compute square root and iverse square root of ivar for flatting.
ivar_flat = ivar.reshape((ivar.shape[0], np.prod(ivar.shape[-2:])))
sqrt_ivar = mat_utils.matpow(ivar_flat, 0.5, return_diag=True)
sqrt_ivar = sqrt_ivar.reshape((ivar.shape[0],) + ivar.shape[-2:])
del ivar_flat, ivar

isqrt_ivar_hp = mat_utils.matpow(ivar_hp, -0.5, return_diag=True)
del ivar_hp

for midx in maps[comm.rank::comm.size]:

    print(comm.rank, f'working on sim {midx}')
    
    # This contains sims for both qids.
    imap = NM.get_sim(args.split_idx, midx, args.lmax, generate=False)[:,0,:,:,:]
    
    for qidx, qid in enumerate(args.qid):
        
        imap[qidx] *= sqrt_ivar[qidx]
        imap_hp = reproject.map2healpix(imap[qidx], nside=nside, extensive=False,
                                        method='harm', lmax=3 * nside, spin=[0, 2])
        imap_hp *= isqrt_ivar_hp[qidx]
        imap_hp *= mask_obs

        # This feels a bit hacky. Just a way to convert qid to freq.
        freq = NM._data_model.get_qid_kwargs_by_subproduct('maps', 'default', qid)['freq']
        
        oname = args.oname_template.format(freq=freq, sidx=args.split_idx, sim_num=midx)
        # Convert to Kelvin.
        imap_hp *= 1e-6
        column_units = 'K'
        hp.write_map(opj(args.odir, oname), imap_hp, overwrite=True, dtype=np.float32,
                     column_units=column_units)

print(comm.rank, 'done')
