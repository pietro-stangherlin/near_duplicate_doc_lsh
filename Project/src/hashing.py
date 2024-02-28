import mmh3
import hashlib
import numpy as np
import ctypes
import os



# ---- generate hash random parameters -------#
def GenerateUns64(num_lists: int,
                  num_elements: int,
                    seed: int) -> list:
        '''Compute list of num_lists lists
        each one of positive with num_elements 64 unsigned bit integer.

        All the integers generated are >= 1.
        Those will be used as parameters for hash functions random parameters
        similar but not limited to:
        where hash(x, A, B) = some_function(A * x + B).

        Args:
        - num_lists: number of lists generated
        - num_elements: number of integers in each list
        - seed: used for reproducibility

        Returns:
            - list of num_lists lists of num_elements unsigned 64 bit integer
        '''

        
        gen = np.random.RandomState(seed)

        max_int = np.iinfo(np.uint64).max

        return [
                [gen.randint(1, max_int, dtype = np.uint64) for _ in range(num_elements)]
                for _ in range(num_lists)
                ]

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
# but it's so slow
def Naive32UniversalHash(x: np.int32,
                       aux_params: list) -> np.uint32:
     '''Performs 2-universal hashing for a 32-bit key.

        Args:
            -x: integer to be hashed
            -aux_params: list two unsigned 64 bit integers
        
        Returns:
            - unsigned 32 bit hashed integer 

        Reference:
        J.Lawrence Carter, Mark N. Wegman, "Universal classes of hash functions"
        Journal of Computer and System Sciences, Volume 18, Issue 2, 1979, Pages 143-154.
     '''
    # mersenne_prime
     p = 2**61 - 1

     a = aux_params[0]
     b = aux_params[1]
     x = np.int64(x)

     # if we want to avoid overflow
     # distributive property of modulo
     # return ((a % p) * (x % p) % p + b % p) % p

     # but beacuse we care only about hash it doesn't matter
     return np.uint32(((a * x + b) % p) % 2**32)


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

def MultiShift32(x: np.uint32,
                  aux_params: list) -> np.uint32:
    '''Applies the operation (a*x + b) mod Prime
    
    Args:
        - x: The 32-bit key.
        - aux_params: list of 2 unsigned 64 bit integers ()
        
    Returns:
        - hash: unsigned 32 bit integer
    
    Instructions:
        compile the file "hashCWtrick32.cpp" as hashCWtrick3.dll,
        example with g++:
        g++ -shared -o hashCWtrick32.dll hashCWtrick32.cpp
    
    All the code used is taken from:
    Mikkel Thorup and Yin Zhang, "Tabulation Based 5-Universal Hashing and Linear Probing",
    2010 Proceedings of the Workshop on Algorithm Engineering and Experiments (ALENEX), pages 62-76.
    table: A.2  plain universal hashing for 32-bit key x.
    '''
    lib.Univ2.argtypes = [ctypes.c_uint32, ctypes.c_uint64, ctypes.c_uint64]
    lib.Univ2.restype = ctypes.c_uint64
    
    A = aux_params[0]
    B = aux_params[1]
    
    return lib.Univ2(x, A, B)

def CWtrick32to32(x: np.uint32,
                  aux_params: list) -> np.uint32:
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
    
    A = aux_params[0]
    B = aux_params[1]
    C = aux_params[2]
    D = aux_params[3]
    E = aux_params[4]
    
    return lib.CWtrick32to32(x, A, B, C, D, E)


def CWtrick32to64(x: np.uint32,
                  aux_params: list) -> np.uint64:
    """
    Applies the operation (a*x + b) mod Prime
    multiple times with different parameters.
    
    Args:
        - x: The 32-bit key.
        - aux_params: list of 5 unsigned 64 bit integers ()
    Returns:
        - hash: unsigned 64 bit integer

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
    lib.CWtrick32to64.argtypes = [ctypes.c_uint32, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
    lib.CWtrick32to64.restype = ctypes.c_uint64
    
    A = aux_params[0]
    B = aux_params[1]
    C = aux_params[2]
    D = aux_params[3]
    E = aux_params[4]
    
    return lib.CWtrick32to64(x, A, B, C, D, E)





# add 64 bit hashing from MIDST project LSH subdirectories




# ----------- LSH bands hash functions ------------------