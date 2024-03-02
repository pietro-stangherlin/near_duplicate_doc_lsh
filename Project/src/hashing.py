import mmh3
import numpy as np
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
            num_rows: number of array's rows
            num_cols: number of array's columns
            reshape: reshape the array into a matrix num_rows * num_cols
            seed: used for reproducibility

        Returns:
            numpy array of dimensions num_rows * num_cols of unsigned 64 bit integer
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
def MurmUns32Hash(input_string: str) -> int:
    '''Compute 32 unsigned int hash (Murmur Hash).

    Reference: https://pypi.org/project/mmh3/

    Args: 
        input_string: string to be hashed
    
    Returns:
        32 bit unsigned integer hash 
    '''
    return mmh3.hash(input_string, signed = False)

# -- Unsigned 64 bit hash Murmur --
def MurmUns64Hash(input_string: str) -> int:
    '''Compute 64 unsigned int hash (Murmur Hash).

    Reference: https://pypi.org/project/mmh3/

    Args: 
        input_string: string to be hashed
    
    Returns:
        64 bit unsigned integer hash 
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

@numba.njit(numba.uint32(numba.uint32, numba.uint64[:]))
def NumbaNaiveHashU32Params(x, params):
    '''Compute unsigned 32bit of unsigned 32 bit integer.
    
    NOTE: 
    a and b should be randomly uniformly generated to get universal hashing
    
    Args:
        x (uint32): integer to be hashed 
        params (array of 2 uint64): params and b in the formula
        
    Returns: 
        hash (uint32): hashed integer
    '''
    x = np.uint64(x)
    p = 2**61 - 1
    return (((params[0] * x + params[1]) % p) % 2**32)

# ----------- LSH bands hash functions ------------------