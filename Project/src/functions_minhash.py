import numpy as np

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


def ComputeHashValues(integer: int,
                      hash_functions_list: list,
                      int_type = np.int16) -> np.array:
    '''Compute array of hash values of shingle.

    Args:
        - integer
        - hash_functions_list: list of hash functions objects
        having input both as input and output
        - int_type: type of integer used in the numpy array
    
    Returns:
        hash_values_array: array of all the hash values

    '''
    k = len(hash_functions_list)

    values = np.empty(shape= k, dtype= int_type)

    for i in range(k):
        values[i] = hash_functions_list[i](integer)
    
    return values

#------------------ Generate Signature ---------------------#
def GenerateSignature(shingles_array: np.array,
                      hash_functions_list: list,
                      hash_functions_dictionary: dict,
                      int_type = np.int16) -> np.array:
    '''Generate signature from shingles array.

        Let k be the number of hash functions in the hash_functions_list.
        The function works on two arrays of length k: one is the signature
        and it's inizialized with all elements set to the
        first shingles_array element, the other
        contains the position of the signature elements
        determined by each hash function (permutation).
        Conditionally on each hash function, for each shingles_array element
        check its permuted position, if smaller than the position stored 
        in the position array -> update that position with it and, in the signature array,
        substitute the corresponding shingle with the current one. 

        Implementation details.
        For each shingles_array element check its presence as a key
        in hash_permutations_dictionary:
        if present then use those values, if not computes the k hashes and
        updates hash_permutations_dictionary adding the array
        to it with the shingle as a key.
    
    Args:
        - shingles_array: array of number of hashed shingles
        - hash_permutations_family:list of k hash functions
        - hash_permutations_dictionary: dictionary where 
                                    key = shingle value
                                    value = np.array of k values (int) where
                                    each value is the result of the j-th
                                    hash function on key
        - int_type: type of integer used in the numpy array

    Returns:
        signature_vector: np.array of k values (int) where
                                    each value is the result of the j-th
                                    hash function on shingles_array
    '''


    hash_num = len(hash_functions_list)

    first_value = shingles_array[0]
    signature = np.full(shape= hash_num,
                        fill_value = first_value,
                        dtype= int_type)

    # first fill
    
    if first_value in hash_functions_dictionary:
        positions = hash_functions_dictionary[first_value]

    else:
        positions = ComputeHashValues(first_value,
                                      hash_functions_list,
                                      int_type)
        # copy the array in a new array
        # or the change in positions will be reflected 
        # on the hash_functions_dictionary array
        hash_functions_dictionary[first_value] = np.array(positions,
                                                          dtype = int_type)
        
    
    # other shingles
    for i in range(1, len(shingles_array)):
        value = shingles_array[i]

        # get positions
        if value in hash_functions_dictionary:
            temp_pos = hash_functions_dictionary[value]
        else:
            temp_pos = ComputeHashValues(value,
                                      hash_functions_list,
                                      int_type)
            hash_functions_dictionary[value] = temp_pos
        
        
        # confront and eventually update positions
        for j in range(hash_num):
            if temp_pos[j] < positions[j]:
                positions[j] = temp_pos[j]
                signature[j] = value

    
    return signature

