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

#------------------ Generate Signature ---------------------#
def GenerateSignature(shingles_array: np.array,
                      hash_functions_list: list,
                      hash_functions_dictionary: dict) -> np.array:
    '''Generate signature from shingles array.

        Let k be the number of hash functions in the hash_functions_list.
        The function works on two arrays of length k: one is the signature
        and it's inizialized with all elements set to the
        first shingles_array element, the other
        contains the position of the signature elements
        determined by each hash function (permutation).
        Conditionally on each hash function for each shingles_array element
        check its permuted position, if its smaller than the position stored 
        in the position array update that osition with it and, in the signature array
        substitute the corresponding shingle with the current one. 

        Implementation details.
        For each shingles_array element checks its presence as a key
        in hash_permutations_dictionary:
        if it is present then use those values, if not computes the k hashes and
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

    Returns:
        signature_vector: np.array of k values (int) where
                                    each value is the result of the j-th
                                    hash function on shingles_array
    '''


    hash_num = len(hash_functions_list)

    signature = np.empty(shape= k, dtype= np.int16)

    # first fill
    for j in range(hash_num):
        signature[j] = shingles_array[0]
    
    if shingles_array[0] in hash_functions_dictionary:
        positions = hash_functions_dictionary[shingles_array[0]]
    else:
        positions = ComputeHashValues(shingles_array[0],
                                      hash_functions_list)
        hash_functions_dictionary[shingles_array[0]] = positions
    
    # other shingles
    for i in range(1, len(shingles_array)):
        el = shingles_array[i]

        # get positions
        if el in hash_functions_dictionary:
            temp_pos = hash_functions_dictionary[el]
        else:
            temp_pos = ComputeHashValues(el,
                                      hash_functions_list)
            hash_functions_dictionary[el] = temp_pos
        
        # confront and eventually update positions
        for j in range(hash_num):
            if temp_pos[j] < positions[j]:
                positions[j] = temp_pos[j]
                signature[j] = el


    return signature




def ComputeHashValues(shingle: int,
                      hash_functions_list: list) -> np.array:
    '''Compute array of hash values of shingle.

    Args:
        - shingle:
        - hash_functions_list:
    
    Returns:
        hash_values_array:

    '''
    k = len(hash_functions_list)

    values = np.empty(shape= k, dtype= np.int16)

    for i in range(k):
        values[i] = hash_functions_list[i](shingle)
    
    return values
