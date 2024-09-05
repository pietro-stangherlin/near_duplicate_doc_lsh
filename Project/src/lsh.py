import numpy as np 
from typing import Callable

# Assuming we have a set of elements with fields: id; signature

# elements needed
# 1) bands to cut the signature
# 2) hash function for each band
# 3) data structure to store the buckets:
#   how - many buckets?


def ComputeHashBand(signature: np.array,
             band_inf_index: int,
             band_sup_index: int,
             doc_id: int,
             hash_fun: Callable) -> tuple:
    '''Compute the hash of a band.
    
    Args:
        signature : signature of the document
        band_inf_index : band's inferior index
        band_sup_index : band's superior index
        doc_id : id of the document
        hash_fun : hash function used
    
    Return:
        tuple: (hash value, doc_id)
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
        '''Insert value in the bucket associated with key
        
        Args:
            key: should be the hash of a band
            value: should be the document id
        '''
        if key in self.buckets:
            self.buckets[key].append(value)
        else:
             self.buckets[key] = [value]
    
    def iter(self):
        '''Iterator that yield all buckets (lists)
        '''
        for key in self.buckets:
            yield self.buckets[key]
    
    def iter_more_than_one(self):
        '''Iterator that yield all buckets (lists) with more than one element
        '''
        for key in self.buckets:
            if len(self.buckets[key]) > 1:
                yield self.buckets[key]
    
    
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
        self.bands_number = bands_number
        self.bands_list = [LSHOneBandBucketsNaive() for _ in range(bands_number)]
    
    def insert (self, band: int, key: int, value: int) -> None:
        '''
        In the specified band, add the value to its key corresponding bucket
        
        Args:
            band: band number
            key: hash value used to get the bucket 
            value: value stored in the bucket (usually doc_id)
    
        '''
        self.bands_list[band].insert(key, value)
    
    def iter_band(self, band : int):
        '''Iterator that yield all buckets (lists) in the band
        '''
        return self.bands_list[band].iter()
    
    def iter_band_more_than_one(self, band : int):
        '''Iterator that yield all buckets (lists) with more than one element
            in the band
        '''
        return self.bands_list[band].iter_more_than_one()
    
    def iter_all_bands(self) -> list:
        '''return list of the iterators for all bands'''
        return [self.iter_band(band) for band in range(self.bands_number)]

    def iter_more_than_one_all_bands(self) -> list:
        '''return list of the iterators for all bands with buckets with more 
        than one element'''
        return [self.iter_band_more_than_one(band) for band in range(self.bands_number)]
        
    
    def __str__(self):
        return str(self.bands_list)