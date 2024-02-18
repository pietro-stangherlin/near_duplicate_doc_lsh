# ---------- Shingle Hash --------------


# ---------- Signature permutation hash functions ---------------

#----------- just used for testing ------------
def ToyHashGen(text: str, hash_parameter: int) -> int:
    '''Sum the numbers code for each character,
    the modulo of the division of the sum by the hash_parameter is the hash

    Args: 
        - text: string to be hashed
        - hash_parameter: modulo of the division

    Returns:
        hash value of object
    '''
    return sum([ord(char) for char in text]) % hash_parameter

def ToyHashListGen(k: int) -> list:
    '''Generate a list of k toy hash functions objects.

    Args:
        - k: number of hash functions 

    Returns: 
        list of of toy hash functions objects
    '''

    # list of toy hashes
    toy_hash_functions_list = [None for i in range(k)]

    # populate the list
    for i in range(k):
        toy_hash_functions_list[i] = lambda x : ToyHashGen(x, i + 1)

    return toy_hash_functions_list





# ----------- LSH bands hash functions ------------------