import mmh3
import hashlib
import numpy as np
import ctypes
import os
import numba



# ---- generate hash random parameters -------#
def GenerateNumpyArray(num_rows: int,
                  num_cols: int,
                  seed: int,
                  reshape: bool,
                  int_type = np.uint64) -> np.array:
        '''Compute array of 64 unsigned bit integer.

        All the integers generated are >= 1.

        Args:
        - num_rows: number of array's rows
        - num_cols: number of array's columns
        - reshape: reshape the array into a matrix num_rows * num_cols
        - seed: used for reproducibility

        Returns:
            - numpy array of dimensions num_rows * num_cols of unsigned 64 bit integer
        '''

        np.random.seed(seed)

        array = np.random.randint(low = 1 ,
                                 high = np.iinfo(int_type).max,
                                 size = num_rows * num_cols,
                                 dtype = int_type)
        # return matrix
        if reshape:
            return array.reshape(num_rows, num_cols)
        
        # return array
        return array

# ---------- Shingle Hash --------------
# -- Unsigned 32 bit hash Murmur --
def MurmUns32Hash(input_string):
    '''Compute 32 unsigned int hash (Murmur Hash).

    Reference: https://pypi.org/project/mmh3/

    Args: 
        - input_string: string to be hashed
    
    Returns:
        - 32 bit unsigned integer hash 
    '''
    return mmh3.hash(input_string, signed = False)

# -- Unsigned 64 bit hash Murmur --
def MurmUns64Hash(input_string):
    '''Compute 64 unsigned int hash (Murmur Hash).

    Reference: https://pypi.org/project/mmh3/

    Args: 
        - input_string: string to be hashed
    
    Returns:
        - 64 bit unsigned integer hash 
    '''
    # mmm3 returns a tuple of two 64 bit hashes
    # only the first is returned here
    return mmh3.hash64(input_string, signed = False)[0]

# ---------- Signature permutation hash functions ---------------
# hash functions serving as row permutations in MinHash:
# MinHash requires the row permutations to be random
# implying the set of hash functions used to simulate the permutations
# should resemble a random extraction.

# --- Universal Hashing families ---
# In order to do this we use families of (near) universal hash functions.
# Reference:
# J.Lawrence Carter, Mark N. Wegman, "Universal classes of hash functions"
# Journal of Computer and System Sciences, Volume 18, Issue 2, 1979, Pages 143-154.

# -- Implementation --
# The main idea is to have a hash function on the form (a*x + b) mod p
# where x is the integer to be hashed,
# a and b are constats extracted uniformly at random
# and p is a prime.
# NOTE: in practice the hash function could be a bit more complicated.

@numba.jit(numba.uint32(numba.uint32, numba.uint64[:]))
def NumbaNaiveHashU32Params(x, params):
    '''Compute unsigned 32bit of unsigned 32 bit integer.
    
    NOTE: a and b should be randomly uniformly generated
        to get universal hashing
    
    Args:
        - x (uint32): integer to be hashed 
        - params (array of 2 uint64): params and b in the formula
        
    Returns: 
        - (uint32) hashed integer
    '''
    x = np.uint64(x)
    p = 2**61 - 1
    return (((params[0] * x + params[1]) % p) % 2**32)

# The implementations use some computational tricks.
# Reference:
# Mikkel Thorup and Yin Zhang, "Tabulation Based 5-Universal Hashing and Linear Probing",
# 2010 Proceedings of the Workshop on Algorithm Engineering and Experiments (ALENEX), pages 62-76



# ---- article trick ----#
# use c++ compiled code ----
# see instructions in the function descprition

# get the absolute path of the cpp program
# so when the function using it (CW..) are called
# python knows where to search for the script


# Get the path of the current script
script_path = os.path.dirname(__file__)

# Join it with the name of the library file
lib_path = os.path.join(script_path, "hashCWtrick32.dll")

# Load the library using the full path
lib = ctypes.CDLL(lib_path)


def CWtrick32to32(x: np.uint32,
                  aux_params: np.array) -> np.uint32:
    """
    Applies the operation (a*x + b) mod Prime
    multiple times with different parameters.
    
    Args:
        - x: The 32-bit key.
        - aux_params: list of 5 unsigned 64 bit integers ()
        
    Returns:
        - hash: unsigned 32 bit integer
    
    Instructions:
        compile the file "hashCWtrick32.cpp" as hashCWtrick3.dll,
        example with g++:
        g++ -shared -o hashCWtrick32.dll hashCWtrick32.cpp

    All the code used is taken from:
    Mikkel Thorup and Yin Zhang, "Tabulation Based 5-Universal Hashing and Linear Probing",
    2010 Proceedings of the Workshop on Algorithm Engineering and Experiments (ALENEX), pages 62-76.
    A.9  CW trick for32-bit keys with prime 2**61 - 1.
    """
    
    # Provide the argument types and return type of the function
    lib.CWtrick32to32.argtypes = [ctypes.c_uint32, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
    lib.CWtrick32to32.restype = ctypes.c_uint64
    
    return lib.CWtrick32to32(x,
                             aux_params[0],
                             aux_params[1],
                             aux_params[2],
                             aux_params[3],
                             aux_params[4])





# add 64 bit hashing from MIDST project LSH subdirectories




# ----------- LSH bands hash functions ------------------