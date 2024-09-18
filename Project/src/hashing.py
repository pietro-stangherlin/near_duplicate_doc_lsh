import mmh3
import numpy as np
import numba
from typing import Callable

# ---------- Shingle Hash --------------#
# generate integer hash from string

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


# ---- generate hash random parameters -------#
# this is used to generate the parameter matrix
# of row permutations hash functions
# example: a hash function has two parameters a and b
# and we want to find say 100 row permutations via hash
# so we make a matrix with 100 rows and 2 columns
# filled with random integers
def GenerateNumpyArray(num_rows: int,
                       num_cols: int,
                       seed: int,
                       reshape = True,
                       int_type = np.uint64) -> np.array:
        '''Compute array of specified bit integer (default 64 bit unsigned integer).

        All the integers generated are >= 1.

        Args:
            num_rows: number of array's rows
            num_cols: number of array's columns
            seed: used for reproducibility
            reshape: reshape the array into a matrix num_rows * num_cols
            int_type: type of int used, numpy types

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


def NaiveHashU32Params(x : np.uint32, params: np.array) -> np.uint32:
    '''Compute unsigned 32bit of unsigned 32 bit integer.
    
    Args:
        x (uint32): integer to be hashed 
        params (array of 2 uint64): params a and b in the formula
    
    NOTE: 
    a and b should be randomly uniformly generated to get universal hashing
        
    Returns: 
        hash (uint32): hashed integer
    '''
    x = np.uint64(x)
    p = 2**61 - 1
    return np.uint32((((params[0] * x + params[1]) % p) % 2**32))

def NaiveHashU64Params(x : np.uint64, params: np.array) -> np.uint64:
    '''Compute unsigned 64 bit of unsigned 64 bit integer.
    
    Args:
        x (uint32): integer to be hashed 
        params (array of 2 uint64): params a and b in the formula
    
    NOTE: 
    a and b should be randomly uniformly generated to get universal hashing
        
    Returns: 
        hash (uint32): hashed integer
    '''
    x = np.uint64(x)
    p = 2**61 - 1
    return np.uint64((((params[0] * x + params[1]) % p) % 2**32))



@numba.njit(numba.uint32(numba.uint32, numba.uint64[:]))
def NumbaNaiveHashU32Params(x, params):
    '''Compute unsigned 32bit of unsigned 32 bit integer.
    
    Args:
        x (uint32): integer to be hashed 
        params (array of 2 uint64): params a and b in the formula
    
    NOTE: 
    a and b should be randomly uniformly generated to get universal hashing
        
    Returns: 
        hash (uint32): hashed integer
    '''
    x = np.uint64(x)
    p = 2**61 - 1
    return (((params[0] * x + params[1]) % p) % 2**32)

# ----------- LSH bands hash function ------------------
def MotwaniBandArrayHash(v: np.array,
                     random_int_array: np.array,  
                     modulo: int):
    '''Implementation of Band hash functions as described by Motwani et. al. article.
    
        Args:
            v: np.array of unsigned integers of length k
            random_int_array: array of (pseudo) random integers of length k
            modulo: biggest possible hash value - 1
        
        Returns:
        
        Description:
            Assume v = [v1, v2, ..., vk] 
            and random_int_array = [a1,...,ak] is an array of random integers,
            the hash is then:
            hash(v) = (a1 * v1 + ... + ak * vk) % modulo
        
        Reference:
             A. Gionis, P. Indyk, and R. Motwani,
             “Similarity search in high dimensions via hashing,”
             Proc. Intl. Conf. on Very Large Databases, pp. 518 529, 1999.
             "Implementation"
            
        
    '''
    # NOTE: the [0] index is used to convert the array to an integer
    return np.dot(v, random_int_array) % modulo