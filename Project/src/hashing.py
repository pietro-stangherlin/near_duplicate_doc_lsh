import mmh3
import hashlib
import numpy as np

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

# -- Unsigned 64 bit hash from hashlib --
def SHA256Uns64Hash(input_string):
    '''Compute 64 unsigned int hash (hashlib.sha256).

    Args: 
        - input_string: string to be hashed
    
    Returns:
        - 64 bit unsigned integer hash 
    '''
    sha_signature = hashlib.sha256(input_string.encode()).digest()

    # Convert to integer and truncate to 64 bits
    int_hash = int.from_bytes(sha_signature, byteorder='big') & ((1 << 64) - 1)

    return int_hash

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

# The implementations use some computational tricks.
# Reference:
# Mikkel Thorup and Yin Zhang, "Tabulation Based 5-Universal Hashing and Linear Probing",
# 2010 Proceedings of the Workshop on Algorithm Engineering and Experiments (ALENEX), pages 62-76

# use this by default
def Naive32UniversalHash(x: np.int32,
                       aux_params: np.array) -> int:
     '''Performs 2-universal hashing for a 32-bit key.

        For this function aux_params should be a numpy array of two unsigned 64 bit integers

        Reference:
        J.Lawrence Carter, Mark N. Wegman, "Universal classes of hash functions"
        Journal of Computer and System Sciences, Volume 18, Issue 2, 1979, Pages 143-154.
     '''
    # mersenne_prime
     p = 2**31 - 1

     a = np.int64(aux_params[0])
     b = np.int64(aux_params[1])
     x = np.int64(x)

     # if we want to avoid overflow
     # distributive property of modulo
     # return ((a % p) * (x % p) % p + b % p) % p

     # but beacuse we care only about hash it doesn't matter
     return (a * x + b) % p



# -- 32 bit keys universal hashing --
# WARNING: needs to be checked
# beacuse it's bad defined
def HashMultShift32(x: np.int32,
                    aux_params: np.array) -> int:
    """
    Performs 2-universal hashing for a 32-bit key.

    For this function aux_params should be a numpy array of two unsigned 64 bit integers

    Reference:
    Mikkel Thorup and Yin Zhang, "Tabulation Based 5-Universal Hashing and Linear Probing",
    2010 Proceedings of the Workshop on Algorithm Engineering and Experiments (ALENEX), pages 62-76.
    A.2  Multiplication-shift based hashing for32-bit keys.


    Args:
    - x: 32-bit int to be hashed.
    - aux_params: numpy array of two unsigned 64 bit integers

    Returns:
    The result of the 2-universal hashing.
    """
    if len(aux_params) != 2:
         print("Error: the aux_params should have only two elements")
         return None

    a = np.int64(aux_params[0])
    b = np.int64(aux_params[1])
    x = np.int64(x)

    # try
    return ((a * x + b)  % (2**61 - 1))

    # debug
    # print(str((a * (x >> 32) + (b >> 32))))
    # Perform operations in a way that avoids intermediate overflow
    # return (a * (x >> 32) + (b >> 32))

    # before was
    # return ((a * x + b) >> 32)


def GenerateTwoUns64(num_tuples: int,
                     seed: int) -> list:
        '''Compute array of num_tuples tuples of positive 64 bit integer.

        The first tuple element is >= 1, the second >= 0.
        Those will be used as parameters for hash functions parameters A and B
        where hash(x, A, B) = some_function(A * x + B).

        Args:
        - num_tuples: number of tuples generated
        - seed: used for reproducibility

        Returns:
            - list of num_tuples tuples of two positive 64 bit integer
        '''

        
        gen = np.random.RandomState(seed)

        max_int = np.iinfo(np.uint64).max

        return [(gen.randint(1, max_int, dtype = np.uint64),
                gen.randint(0, max_int, dtype = np.uint64))
                for _ in range(num_tuples)]



# add 64 bit hashing from MIDST project LSH subdirectories




# ----------- LSH bands hash functions ------------------