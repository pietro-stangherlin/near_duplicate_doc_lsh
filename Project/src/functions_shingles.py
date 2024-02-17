from typing import Callable
import numpy as np

def TextToShinglesArray(text: str,
                        shingle_len: int,
                        hash_fun: Callable) -> np.array:
    '''Compute all the shingles of size shingle_len, hash them 
        and save the result in a numpy array

    Examples:
        >>> TextToShinglesArray("abcdf", 3, lambda x : sum([ord(c) for c in x]) % 5)
        array([4, 2, 1], dtype=int16)

    Args:
        text: text from which to compute she shingles
        shingle_len: each shingle length
        hash_fun: hash function applied to each shingle

    Returns:
        np.array of ints of hashed shingles
    '''
    # number of possibile consecutive shingles of the chosen length
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
        >>> TextToShinglesSet("abcdf", 3, lambda x : sum([ord(c) for c in x]) % 5)
        {1, 2, 4}

    Args:
        text: text from which to compute she shingles
        shingle_len: each shingle length
        hash_fun: hash function applied to each shingle

    Returns:
        set of ints of hashed shingles
    '''
    # number of possibile consecutive shingles of the chosen length
    shingles_num = len(text) - shingle_len + 1
    # allocate empty set
    shingles_set = set()
    
    for i in range(shingles_num):
        shingles_set.add(hash_fun(text[i:i + shingle_len]))
    
    return shingles_set


if __name__ == "__main__":
    pass