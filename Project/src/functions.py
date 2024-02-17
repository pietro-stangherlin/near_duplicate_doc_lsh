from typing import Callable
import hashlib as hsl
import numpy as np

# --------------------- Shingles --------------------------#

def TextToShinglesArray(text: str,
                        shingle_len: int,
                        hash_fun: Callable) -> np.array:
    '''Compute all the shingles of size shingle_len, hash them 
        and save the result in an numpy array

    Examples:
        >>> TextToShinglesArray("abcdf", 3, lambda x : hash(x) % 5)
        array([0, 1, 2], dtype=int16)

    Args:
        text: text from which to compute she shingles
        shingle_len: each shingle lenght
        hash_fun: hash function applied to each shingle

    Returns:
        np.array of ints of hashed shingles
    '''
    # number of possibile consecutive shingles of the chosen lenght
    shingles_num = len(text) - shingle_len + 1
    # allocate empty array
    shingles_array = np.empty(shape= shingles_num, dtype= np.int16)
    
    for i in range(shingles_num):
        shingles_array[i] = hash_fun(text[i:i + shingle_len])
    
    return shingles_array
    

def TextToShinglesSet(text: str,
                        shingle_len: int,
                        hash_fun: Callable) -> set:
    '''Compute all the shingles of size shingle_len, hash them 
        and save the result in an set

    Examples:
        >>> TextToShinglesSet("abcdf", 3, lambda x : hash(x) % 5)
        {0, 1, 2}

    Args:
        text: text from which to compute she shingles
        shingle_len: each shingle lenght
        hash_fun: hash function applied to each shingle

    Returns:
        set of ints of hashed shingles
    '''
    # number of possibile consecutive shingles of the chosen lenght
    shingles_num = len(text) - shingle_len + 1
    # allocate empty set
    shingles_set = set()
    
    for i in range(shingles_num):
        shingles_set.add(hash_fun(text[i:i + shingle_len]))
    
    return shingles_set


if __name__ == "__main__":
    pass