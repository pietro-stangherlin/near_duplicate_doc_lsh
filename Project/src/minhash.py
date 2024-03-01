import numpy as np
import numba
from typing import Callable
from BTrees._LOBTree import LOBTree

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

#------------------ Generate Signature ---------------------#
@numba.jit
def NumbaSignatureByRow(shingles_array: np.array,
                              hash_params_matrix: np.array,
                              hash_fun: Callable,
                              int_type: np.uint32):
    '''Computes signature array.
    
    Args:
        - shingles_array: numpy array of shingles (integers)
        - hash_params_matrix: matrix of parameters (other than the hashable)
                            used to compute the hash function,
                            each row corresponds to a set of parameters
                            for a different hash function accepting
                            a number of auxiliary parameters equals to 
                            the columns number
        - hash_fun: the hash function used, note that at the moment
                    is not implemented any compatibility check between
                    the paramters of this function and those of 
                    the hash_function
        - int_type: integer type of the signature elements
        
    Returns:
        - signature array
    '''
    num_matrix_rows = hash_params_matrix.shape[0]
    signature = np.full(shape = num_matrix_rows,
                        fill_value = np.iinfo(int_type).max)
    
    for row_index in range(num_matrix_rows):
        for shingle in shingles_array:
            value = hash_fun(shingle, hash_params_matrix[row_index])
            if value < signature[row_index]:
                signature[row_index] = value
    
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
