import mmh3
import hashlib
import numpy as np

# ---------- Shingle Hash --------------
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
# Universal Hashing
# add 32 bit hashing from datasketch
# add 64 bit hashing from MIDST progject LSH subdirectories



#----------- just used for testing ------------
def ToyHashGen(text: str, hash_parameter: int) -> int:
    '''Sum the numbers code for each character,
    the modulo of the division of the sum by the hash_parameter is the hash

    Args: 
        - text: string to be hashed
        - hash_parameter: modulo of the division

    Returns:
        - hash value of object
    '''
    return sum([ord(char) for char in text]) % hash_parameter

def ToyHashListGen(k: int) -> list:
    '''Generate a list of k toy hash functions objects.

    Args:
        - k: number of hash functions 

    Returns: 
        - list of of toy hash functions objects
    '''

    # list of toy hashes
    toy_hash_functions_list = [None for i in range(k)]

    # populate the list
    for i in range(k):
        toy_hash_functions_list[i] = lambda x : ToyHashGen(x, i + 1)

    return toy_hash_functions_list





# ----------- LSH bands hash functions ------------------