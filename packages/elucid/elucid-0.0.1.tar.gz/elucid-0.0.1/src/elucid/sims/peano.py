from __future__ import annotations
import typing
from typing import Self
import numpy as np
import numba
from numba.experimental import jitclass

@jitclass
class Peano:
    '''
    Peano-Hilbert (PH) curve implementation. Copied and rewritten from Gadget-2 
    (Volker Springel et al. 2025, MNRAS 364, 1105).
    
    For ELUCID, we adopted bits = 8 (i.e. 256 cells on a side of the simulation
    box).
    '''
    quadrants: numba.int64[:, :, :, :]
    rotxmap_table: numba.int64[:]
    rotymap_table: numba.int64[:]
    rotx_table: numba.int64[:]
    roty_table: numba.int64[:]
    sense_table: numba.int64[:]
    bits: numba.int64

    def __init__(self, bits):
        self.bits = bits

        self.quadrants = np.array([
            [[[0, 7], [1, 6]], [[3, 4], [2, 5]]],
            [[[7, 4], [6, 5]], [[0, 3], [1, 2]]],
            [[[4, 3], [5, 2]], [[7, 0], [6, 1]]],
            [[[3, 0], [2, 1]], [[4, 7], [5, 6]]],
            [[[1, 0], [6, 7]], [[2, 3], [5, 4]]],
            [[[0, 3], [7, 4]], [[1, 2], [6, 5]]],
            [[[3, 2], [4, 5]], [[0, 1], [7, 6]]],
            [[[2, 1], [5, 6]], [[3, 0], [4, 7]]],
            [[[6, 1], [7, 0]], [[5, 2], [4, 3]]],
            [[[1, 2], [0, 3]], [[6, 5], [7, 4]]],
            [[[2, 5], [3, 4]], [[1, 6], [0, 7]]],
            [[[5, 6], [4, 7]], [[2, 1], [3, 0]]],
            [[[7, 6], [0, 1]], [[4, 5], [3, 2]]],
            [[[6, 5], [1, 2]], [[7, 4], [0, 3]]],
            [[[5, 4], [2, 3]], [[6, 7], [1, 0]]],
            [[[4, 7], [3, 0]], [[5, 6], [2, 1]]],
            [[[6, 7], [5, 4]], [[1, 0], [2, 3]]],
            [[[7, 0], [4, 3]], [[6, 1], [5, 2]]],
            [[[0, 1], [3, 2]], [[7, 6], [4, 5]]],
            [[[1, 6], [2, 5]], [[0, 7], [3, 4]]],
            [[[2, 3], [1, 0]], [[5, 4], [6, 7]]],
            [[[3, 4], [0, 7]], [[2, 5], [1, 6]]],
            [[[4, 5], [7, 6]], [[3, 2], [0, 1]]],
            [[[5, 2], [6, 1]], [[4, 3], [7, 0]]]
        ])

        self.rotxmap_table = np.array(
            [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 17, 18, 19,
             16, 23, 20, 21, 22])
        self.rotymap_table = np.array(
            [1, 2, 3, 0, 16, 17, 18, 19, 11, 8, 9, 10, 22, 23, 20, 21, 14, 15,
             12, 13, 4, 5, 6, 7])
        self.rotx_table = np.array([3, 0, 0, 2, 2, 0, 0, 1])
        self.roty_table = np.array([0, 1, 1, 2, 2, 3, 3, 0])
        self.sense_table = np.array([-1, -1, -1, +1, +1, -1, -1, -1])

    def peano_hilbert_keys(self, xs):
        n = len(xs)
        keys = np.zeros(n, dtype=np.int64)
        for i, (_x, _y, _z) in enumerate(xs):
            keys[i] = self.peano_hilbert_key(_x, _y, _z)
        return keys

    def peano_hilbert_key(self, x, y, z):
        x, y, z = np.int64(x), np.int64(y), np.int64(z)
        mask = 1 << (self.bits - 1)
        key = 0
        rotation = 0
        sense = 1

        for i in range(self.bits):
            bitx = 1 if x & mask != 0 else 0
            bity = 1 if y & mask != 0 else 0
            bitz = 1 if z & mask != 0 else 0

            quad = self.quadrants[rotation][bitx][bity][bitz]
            key <<= 3
            key += (quad if sense == 1 else 7 - quad)

            rotx = self.rotx_table[quad]
            roty = self.roty_table[quad]
            sense *= self.sense_table[quad]

            while rotx > 0:
                rotation = self.rotxmap_table[rotation]
                rotx -= 1

            while roty > 0:

                rotation = self.rotymap_table[rotation]
                roty -= 1

            mask >>= 1

        return key