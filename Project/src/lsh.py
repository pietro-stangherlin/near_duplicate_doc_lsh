import numpy as np 
from typing import Callable
from BTrees._LOBTree import LOBTree
from . import sqlite_one_table
from . import hashing

# Assuming we have a set of elements with fields: id; signature

# elements needed
# 1) bands to cut the signature
# 2) hash function for each band
# 3) data structure to store the buckets:
#   how - many buckets?


def ComputeHashBand(signature: np.array,
             band_inf_index: int,
             band_sup_index: int,
             hash_fun: Callable) -> int:
    '''Compute the hash of a band.
    
    Args:
        - signature : signature of the document
        - band_inf_index : band's inferior index
        - band_sup_index : band's superior index
        - hash_fun : hash function used
    
    Return:
        hash value (int)
    '''
    return int(hash_fun(signature[band_inf_index : band_sup_index]))



def GenerateMotwaniHashFunctionsList(n_hash_functions: int,
                                     band_size: int,
                                     modulo: int,
                                     seed: int) -> list:
    '''Generate a list of "Motwani" hash functions, each hash function is assumed to receive an input 
    of size band_size (np.array).
    
    Args:
        - n_hash_functions (int): number of hash functions 
        - band_size (int): size of each band
        - modulo: modulo used (same for each hash function)
        - seed (int): use for reproducibility
    
    Returns:
        - (list) list of hash functions, each one has a different set of parameters
    '''
    # each row corresponds to a set of parameters
    param_matrix = hashing.GenerateNumpyArray(num_rows = n_hash_functions,
                                              num_cols = band_size,
                                              seed = seed)
    # returned function
    functions_list = [None for i in range(n_hash_functions)]
    
    
    for i in range(len(functions_list)):
        functions_list[i] = hashing.GenerateOneMotwaniHash(params = param_matrix[i,],
                                                           modulo = modulo)
    
    return functions_list
    


# ---------------- LSH bands BTree data structure ------------------- # 

# --------- LSH one band buckets BTree data structure --------------- # 
class LSHOneBandBucketsBTree(LOBTree):
    '''BTree used to store buckets for one LSH band.
    The key is the bucket id, value is a set of document ids.
    
    Inherit the IOBTree class from BTrees module: 
    https://btrees.readthedocs.io/
    
    Args: 
        key (unsigned_integer): bucket id
        value (set): set of doc ids
    '''
    # change if necessary
    # max number of elements a leaf can have
    max_leaf_size = 500
    # max number of children an interior node could have
    max_internal_size = 1000
    
    # adding an attribute to the class:
    # set of id_buckets (keys) for buckets with two or more elements
    # this way, when we search for buckets with more than one elements we already know where their indexes
    more_than_two_buckets_ids_set = set()

    def add_ids_pair(self, id_bucket: int, id_doc: int) -> None:
        '''Add a document id to the specific bucket.
        If id_bucket is already in the Btree, add id_doc to its set,
        else add id_bucket first as key and then allocate the set with id_doc as element 
    
        Args:
            - id_bucket (int): id of the bucket
            - id_doc (int):  id of the document
    
        Returns:
            - None
        '''
        
        if id_bucket not in self:
            self.insert(id_bucket, set([id_doc]))
        
        else:
            self[id_bucket].add(id_doc)
            
            # if the set already exists it means now has at least two elements
            self.more_than_two_buckets_ids_set.add(id_bucket)
    
    def return_more_than_one_buckets_ids(self) -> set:
        '''Return a set of all buckets ids for buckets with at least two elements
        '''
        return self.more_than_two_buckets_ids_set

# --------- LSH many bands buckets BTree data structure --------------- # 

class LSHManyBandsBucketsBTree:
    
    def __init__(self,
                 hash_functions_list: list,
                 band_size: int) -> LSHOneBandBucketsBTree:
        '''Generate an instance of an object containig many LSHOneBandBucketsBTree instances
        
        Args:
            - hash_functions_list: list of functions, each function is used to determine the hash
            for a specific band. From this list length is inferred the number of bands
            - band_size (int): band size, with the constraint that each band has the same size 
        
        Return:
            - instance of LSHManyBandsBucketsBTree class
        '''
        self.hash_functions_list = hash_functions_list
        self.n_bands = len(hash_functions_list)
        
        self.band_size = band_size
        
        self.signature_len = self.band_size * self.n_bands
        
        # initialize all the instances
        self.bands_object_list = [LSHOneBandBucketsBTree() for i in range(self.n_bands)]
    
    def __str__(self) -> str:
        '''Print the number of bands
        '''
        print(f"number of bands: {self.n_bands}")
    
    def InsertHashInEachBand(self,
                         signature: np.array,
                         id_doc: int) -> None:
        '''Given an input signature compute the hash for each band and store it
        in their associated data structure.
        
        Args: 
            - signature: np.array 
            - id_doc: document id
            
        Returns:
            - None
        '''
        # used to iterate through all bands
        band_index = 0
        for i in range(0, # start
                       self.signature_len, # stop
                       self.band_size): # step
            
            self.bands_object_list[band_index].add_ids_pair(id_bucket = ComputeHashBand(signature = signature,
                                                                                        band_inf_index = i,
                                                                                        band_sup_index = i + self.band_size,
                                                                                        hash_fun = self.hash_functions_list[band_index]),
                                                            id_doc = id_doc)
            
            band_index += 1
    
    
# ---------------- LSH bands SQL data structure ------------------- # 