from typing import Callable
import numpy as np

# I should add specifif rolling hashing implementations

def TextToShinglesDuplicates(text: str,
                        shingle_len: int,
                        hash_fun: Callable,
                        int_type = np.uint64) -> np.array:
    '''Compute all the shingles of size shingle_len, hash them 
        and save the result in a numpy array

    Examples:
        >>> TextToShinglesDuplicates("abcdf", 3, lambda x : sum([ord(c) for c in x]) % 5)
        array([4, 2, 1], dtype=int16)

    Args:
        text: text from which to compute she shingles
        shingle_len: each shingle length
        hash_fun: hash function applied to each shingle
        int_type: type of integere used in the numpy array

    Returns:
        array: (numpy.array) array of ints of hashed shingles
    '''
    # number of possibile consecutive shingles of the chosen length
    shingles_num = len(text) - shingle_len + 1
    # allocate empty array
    shingles_array = np.empty(shape= shingles_num, dtype= int_type)
    
    for i in range(shingles_num):
        shingles_array[i] = hash_fun(text[i:i + shingle_len])
    
    return shingles_array
    

def TextToShinglesUniques(text: str,
                        shingle_len: int,
                        hash_fun: Callable) -> set:
    '''Compute all the shingles of size shingle_len,
        return a set of uniques hashed shingles

    Examples:
        >>> TextToShinglesUniques("abcdf", 3, lambda x : sum([ord(c) for c in x]) % 5)
        {1, 2, 4}

    Args:
        text: text from which to compute she shingles
        shingle_len: each shingle length
        hash_fun: hash function applied to each shingle
        int_type: type of integere used in the numpy array

    Returns:
        set of uniques hashed shingles
    '''
    # number of possibile consecutive shingles of the chosen length
    shingles_num = len(text) - shingle_len + 1
    # allocate empty set
    shingles_set = set()
    
    for i in range(shingles_num):
        shingles_set.add(hash_fun(text[i:i + shingle_len]))
    
    return shingles_set