import numpy as np

import numba

import ctypes

from .const import *


def _overflow(x):
    # Since normal python ints and longs can be quite humongous we have to use
    # self hack to make them be able to _overflow.
    # Using a np.int64 won't work either, as it will still complain with:
    # "_overflowError: int too big to convert"
    return ctypes.c_int64(x).value

def gen_permu(seed):
    # Have to zero fill so we can properly loop over it later
    perm = np.zeros(256, dtype=np.int64)
    perm_grad_index3 = np.zeros(256, dtype=np.int64)
    source = np.arange(256)
    # Generates a proper permutation (i.e. doesn't merely perform N
    # successive pair swaps on a base array)
    hashed_seed = _overflow(seed * 6364136223846793005 + 1442695040888963407)
    hashed_seed = _overflow(hashed_seed * 6364136223846793005 + 1442695040888963407)
    hashed_seed = _overflow(hashed_seed * 6364136223846793005 + 1442695040888963407)
    
    for i in range(255, -1, -1):
        hashed_seed = _overflow(hashed_seed * 6364136223846793005 + 1442695040888963407)
        r = int((hashed_seed + 31) % (i + 1))
        if r < 0:
            r += i + 1
        perm[i] = source[r]
        perm_grad_index3[i] = int((perm[i] % (len(GRADIENTS3) / 3)) * 3)
        source[r] = source[i]

    return perm, perm_grad_index3

@numba.njit(cache=True)
def extrapolate2(perm, xsb, ysb, dx, dy):
    index = perm[(perm[xsb & 0xFF] + ysb) & 0xFF] & 0x0E
    g1, g2 = GRADIENTS2[index : index + 2]
    return g1 * dx + g2 * dy


@numba.njit(cache=True)
def extrapolate3(perm, perm_grad_index3, xsb, ysb, zsb, dx, dy, dz):
    index = perm_grad_index3[(perm[(perm[xsb & 0xFF] + ysb) & 0xFF] + zsb) & 0xFF]
    g1, g2, g3 = GRADIENTS3[index : index + 3]
    return g1 * dx + g2 * dy + g3 * dz


@numba.njit(cache=True)
def extrapolate4(perm, xsb, ysb, zsb, wsb, dx, dy, dz, dw):
    index = perm[(perm[(perm[(perm[xsb & 0xFF] + ysb) & 0xFF] + zsb) & 0xFF] + wsb) & 0xFF] & 0xFC
    g1, g2, g3, g4 = GRADIENTS4[index : index + 4]
    return g1 * dx + g2 * dy + g3 * dz + g4 * dw