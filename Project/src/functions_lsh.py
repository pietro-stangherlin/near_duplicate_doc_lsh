import numpy as np 
from typing import Callable

# elements needed
# 1) bands to cut the signature
# 2) hash function for each band
# 3) data structure to store the buckets:
#   how - many buckets?


def HashBand(signature: np.array,
             band_inf_index : int,
             band_sup_index: int,
             doc_id: int,
             hash_fun: Callable) -> tuple:
    '''Compute the hash of a band.
    
    Args:
        - signature : signature of the document
        - band_inf_index : band's inferior index
        - band_sup_index : band's superior index
        - doc_id : id of the document
        - hash_fun : hash function used
    
    Return:
        - tuple: (hash value, doc_id)
    '''
    return (hash_fun(signature[band_inf_index : band_sup_index]), doc_id)
    
    
# ---------------- Naive Buckets --------------------
class LSHOneBandBucketsNaive:
    '''
    The set of buckets is a dictionary
    with key: hash_value, value : list of doc_id (to be changed in numpy array)
    '''
        
    def __init__(self) -> None:
        self.buckets = dict()
    
    def insert(self, key: int, value: int) -> None:
        if key in self.buckets:
            self.buckets[key].append(value)
        else:
             self.buckets[key] = [value]
    
    def __str__(self) -> str:
        return_string = ""
        for key in self.buckets.keys:
            return_string += str(key) + "   " + str(self.buckets[key]) + "\n"
        
        return return_string
    

class LSHAllBandsBucketsNaive:
    '''
    Set of LSHOneBandBucketsNaive (implemented as a list of them)
    '''
    
    def __init__(self, bands_number : int) -> None:
        self.bands_list = [LSHOneBandBucketsNaive() for _ in bands_number]
    
    def __str__(self):
        return str(self.bands_list)
    
    def update (self, band: int, key: int, value: int) -> None:
        '''
        In the specified band, add the value to its key corresponding bucket
        
        Args:
            - band: band number
            - key: hash value used to get the bucket 
            - value: value stored in the bucket (usually doc_id)
    
        '''
        self.bands_list[band].insert(key, value)
    