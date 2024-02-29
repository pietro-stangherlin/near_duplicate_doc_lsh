import numpy as np
from typing import Callable
from BTrees._LOBTree import LOBTree
from multiprocessing import Pool

# requires: family of hash functions
# for both Minhash signatures and LSH bands

# assuming to read file line by line
# and keeping ids
# idea: use shingle to build minhash then delete the shingle
# after each minhash is made:
# populate the buckets of LSH with ids

# Storage of signatures: there are two choices here
# 1) precision wise: save each signature
# in the central memory or, if it's not feasible in storage memory
# 2) after each signatures is used for LSH delete it

def SignatureSimilarity(sig1: np.array, sig2: np.array) -> float:
    '''Compare two signatures element by element and  return the similiraty
    
    Args:
        - sig1: signature 1 (array of len k)
        - sig2: signature 2 (array of len k)
    
    Returns: 
            number positions with the same elements / total positions number
    '''
    l1 = len(sig1)
    l2 = len(sig2)
    
    if l1 != l2:
        print("Error: signatures have different lengths")
        return 0
    
    equals = 0
    for i in range(l1):
        equals += int(sig1[i] == sig2[i])
    
    return equals / l1

def ComputeHashValuesV2(integer: int,
                      hash_function: Callable,
                      hash_params_array: np.array,
                      int_type = np.int64) -> np.array:
    '''Compute array of hash values of shingle.
    
    It's used in the next functions to calculate the permutaions 
    in the signature.

    Example (but non limited to): hash(x, hash_params) = (x*hash_params[0] + hash_params[1]) % 5.
    hash_params_list = [(3, 8), (7, 2)]

    Args:
        - integer: input to be hashed by all hash functions in the list.
        - hash_function: hash functions object, accepts (x, hash_params)
                        where x is the element to be hashed.
        - hash_params_array: hash_params_list is a list of list, each one 
                            containing a set of parameters used for the hash function.
        - int_type: type of integer used in the numpy array.

    
    Returns:
        hash_values_array: array of all the hash values

    '''
    
    return np.apply_along_axis(hash_function,
                                 axis = 1,
                                 arr = hash_params_array,
                                 x = integer)

#------------------ Generate Signature ---------------------#

def GenerateSignatureV2(shingles: iter,
                      hash_function: Callable,
                      hash_params_list: list,
                      use_permutations_dict: bool = False,
                      permutations_dict: dict = None,
                      int_type = np.int64) -> np.array:
    '''Generate signature from shingles array.

        Let k be the number of hash functions elements the hash_params_list.
        The function works on two arrays of length k: one is the signature
        and it's inizialized with all elements set to the
        first shingles_array element, the other
        contains the position of the signature elements
        determined by each hash function (permutation).
        Conditionally on each hash function (each element of hash_params_list), for each shingles element
        check its permuted position, if smaller than the position stored 
        in the position array -> update that position with it and, in the signature array,
        substitute the corresponding shingle with the current one. 

        Implementation details.
        If se_permutations_dict is True:
            For each shingles element check its presence as a key
            in hash_permutations_dict:
            if present use those values, if not computes the k hashes and
            updates hash_permutations_dict adding the array
            to it with the shingle as a key.
        Else (default) don't check for the dictionary and just compute each permutation
    
    Args:
        - shingles: iterable object (list, set, numpy.array...) containing hashed shingles.
        - hash_function: hash functions object, accepts (x, hash_params)
                        where x is the element to be hashed.
        - hash_params_list: hash_params_list is a list of list, each one 
                            containing a set of parameters used for the hash function.
        - use_permutations_dict: Use or not a dictionary to store
                                    all the previous permutations (see implementation details).
        - permutations_dict: dictionary where 
                                    key = shingle value
                                    value = np.array of k values (int) where
                                    each value is the result of the j-th
                                    hash function on key.
        - int_type: type of integer used in the numpy array.

    Returns:
        signature_vector: np.array of k values (int) where
                                    each value is the result of the j-th
                                    hash function on shingles_array.
    '''


    num_hash_funs = len(hash_params_list)
    
    # allocate signature matrix
    signature = np.zeros(shape = num_hash_funs,
                        dtype = int_type)
 
    # allocate permuted positions array
    # fill it with the maximum int_type integer
    # so it's surely greater or equal than the hashed values
    # (assuming the hash functions generate smaller integers than max(int_type))
    positions = np.full(shape = num_hash_funs,
                        fill_value = np.iinfo(int_type).max,
                        dtype = int_type)

    for value in shingles:
        
        if use_permutations_dict:
            if value in permutations_dict:
                temp_permuted_pos = permutations_dict[value]
            else:
                temp_permuted_pos = ComputeHashValuesV2(value,
                                        hash_function,
                                        hash_params_list,
                                        int_type)
                permutations_dict[value] = temp_permuted_pos
        
        else:
            temp_permuted_pos = ComputeHashValuesV2(value,
                                        hash_function,
                                        hash_params_list,
                                        int_type)
            
            
        
        
        # confront and eventually update positions and signature
        for hash_fun_index in range(num_hash_funs):
            if temp_permuted_pos[hash_fun_index] < positions[hash_fun_index]:
                positions[hash_fun_index] = temp_permuted_pos[hash_fun_index]
                signature[hash_fun_index] = value

    
    return signature


def hash_with_params(args):
    hash_function, value, params = args
    return hash_function(value, params)

# no dictionary used
def GenerateSignatureV3(shingles: iter,
                      hash_function: Callable,
                      hash_params_array: np.array,
                      int_type = np.int64) -> np.array:
    '''Generate signature from shingles array.

        Let k be the number of hash functions elements.
        The function works on two arrays of length k: one is the signature
        and it's inizialized with all elements set to the
        first shingles_array element, the other
        contains the position of the signature elements
        determined by each hash function (permutation).
        Conditionally on each hash function (each element of hash_params_list), for each shingles element
        check its permuted position, if smaller than the position stored 
        in the position array -> update that position with it and, in the signature array,
        substitute the corresponding shingle with the current one. 
    
    Args:
        - shingles: iterable object (list, set, numpy.array...) containing hashed shingles.
        - hash_function: hash functions object, accepts (x, hash_params)
                        where x is the element to be hashed.
        - hash_params_array: 2D array 
                            each row has a set of parameters for the hash function 
        - int_type: type of integer used in the numpy array.

    Returns:
        signature_vector: np.array of k values (int) where
                                    each value is the result of the j-th
                                    hash function on shingles_array.
    '''

    num_hash_funs = hash_params_array.shape[1]
    
    # allocate signature matrix
    signature = np.zeros(shape = num_hash_funs,
                        dtype = int_type)
 
    # allocate permuted positions array
    positions = np.full(shape = num_hash_funs,
                        fill_value = np.iinfo(int_type).max,
                        dtype = int_type)

    # Create a pool of processes
    for value in shingles:
        # Compute hash values in parallel
        temp_permuted_pos = ComputeHashValuesV2(value,
                                    hash_function,
                                    hash_params_array,
                                    int_type)
            
        # Vectorized comparison and update
        mask = temp_permuted_pos < positions
        positions[mask] = temp_permuted_pos[mask]
        signature[mask] = value

    return signature

# --------- Signatures set data structure ---------------

class SignaturesBTree(LOBTree):
    '''BTree used to store doc id as keys and doc signatures as values.
    
    Inherit the IOBTree class from BTrees module: 
    https://btrees.readthedocs.io/
    
    Args: 
        - key: Unsigned integer (doc id)
        - value: np.array of int (doc signature)
    '''
    # change if necessary
    # max number of elements a leaf can have
    max_leaf_size = 500
    # max number of childern an interior node could have
    max_internal_size = 1000
