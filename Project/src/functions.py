import json
import hashlib as hsl
import numpy as np

# --------------------- Shingles --------------------------#
# Choose between these two functions
def TextToShinglesArray(text, shingle_len, hash_fun, do_hash = True):
    '''
    @param text (str)
    @param shingle_len (int)
    @param hash_fun (fun): hash applied to each shingle
    @param do_hash (bool): apply hash to each shingle (True preferred)

    @return (np.array of ints): array of shingles (int) if do_hash = True,
                                 else list of shingles (str)
                                 only recommended for debugging
    '''
    shingles_num = len(text) - shingle_len + 1

    if do_hash == True:
        shingles_array = np.empty(shape= shingles_num, dtype= np.int16)
    
    else:
        shingles_array = list(None for i in range(shingles_num))
        # the hash function just maps the string to itself
        hash_fun = lambda x: x
        

    for i in range(shingles_num):
        shingles_array[i] = hash_fun(text[i:i + shingle_len])
    
    return shingles_array
    



def TextToShinglesSet(text, shingle_len, hash_fun, do_hash = True):
    '''
    @param text (str)
    @param shingle_len (int)
    @param do_hash (bool): apply hash to each shingle (True preferred)

    @return (set of ints): set of shingles (int) if do_hash = True,
                                 else list of shingles (str)
                                 only recommended for debugging
    '''
    shingles_num = len(text) - shingle_len + 1
    shingles_set = set()

    if do_hash == False:
        hash_fun = lambda x : x
    
    for i in range(shingles_num):
        shingles_set.add(hash_fun(text[i:i + shingle_len]))
    
    return shingles_set






if __name__ == "__main__":
    pass