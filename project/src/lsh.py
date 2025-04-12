import numpy as np 
from typing import Callable
from itertools import combinations
from collections import defaultdict

from BTrees._LOBTree import LOBTree
from . import sqlite_one_table
from . import hashing

import subprocess #used to call sqlite dot-command
# see: https://stackoverflow.com/questions/2346074/execute-sqlite3-dot-commands-from-python-or-register-collation-in-command-line

# Assuming we have a set of elements with fields: id; signature

# elements needed
# 1) bands to cut the signature
# 2) hash function for each band
# 3) data structure to store the buckets:
#   how - many buckets?


def ComputeHashBand(signature: np.array,
             band_inf_index: int,
             band_sup_index: int,
             hash_fun: Callable):
    '''Compute the hash of a band.
    
    Args:
        - signature: signature of the document
        - band_inf_index: band's inferior index
        - band_sup_index: band's superior index (not included)
        - hash_fun: hash function used
    
    Return:
        hash value (int)
    '''
    return int(hash_fun(signature[band_inf_index : band_sup_index]))


# NOTE: this way we let each band having its unique hash function
# we get the same hash function for each band as a particular case
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
    # returned functions
    functions_list = [None for i in range(n_hash_functions)]
    
    
    for i in range(len(functions_list)):
        functions_list[i] = hashing.GenerateOneMotwaniHash(params = param_matrix[i,],
                                                           modulo = modulo)
    
    return functions_list

# trivial function, used to skip a check for each document
def GenerateBreakPoints(n: int, n_bands: int) -> list:
    '''Goal: cut an object having length n into n_bands.
    Using Python convenctions: starting with 0 and upper extreme is not included
    Examples: 
       - n is multiple of n_bands: n = 9, n_bands = 3 -> [(0,3), (3,6), (6,9)]
       - n is not multiple of n_bands: n = 9, n_bands = 2 -> [(0,4), (4,8)] (last one is excluded)
    
    Args:
        - n (int): length of the object
        - n_bands (int): number of bands in which the object is cut
    '''
    if n < n_bands:
        print("Error: n_bands cannot be greater than n, return None")
        return None
    
    step_size = n // n_bands
    
    extremes = [i for i in range(0, n, step_size)]
    
    cut_points = [(extremes[i-1], extremes[i]) for i in range(1, len(extremes))]
    
    
    if n % n_bands == 0:
        cut_points.append((extremes[-1], n))
    
    # last check
    if len(cut_points) != n_bands:
        print(f"Warning: cut_points length ({len(cut_points)}) is different from n_bands, return None")
        return None
    
    return cut_points
        

def ComputeAllHashBands(signature: np.array,
                        break_points: list,
                        hash_functions_list: list) -> list:
    '''Given a signature compute the hash (i.e id bucket) for each band using its specific hash function.
    Args:
        - signature (np.array)
        - break_points: list of tuples, each with the extremes of each band.
            Example: n = 9, n_bands = 2 -> [(0,4), (4,8)] (last one is excluded)
        - hash_functions_list (list of functions): each element is a function taking the signature as input,
        assuming hash parameters are already inside the function
    
    Return:
        - list of len n_bands (list of int): each element is a band hash (i.e. bucket id)
    
    WARNING: the function assumes each band has the SAME number of vectors,
    since we have control over the number of elements in each signature 
    and on the number of bands this shouldn't be a problem;
    otherwise the last band of different dimension is just discarded from the LSH computations
    '''
    if len(break_points) != len(hash_functions_list):
        print(f'''Warning: length of break_points ({len(break_points)})
              is different from length of hash_functions_list (f{len(hash_functions_list)}).
              Returning None''')
        return None
    
    bucket_ids_list = [None for i in range(len(break_points))]
    for i in range(len(break_points)):
        bucket_ids_list[i] = ComputeHashBand(signature = signature,
                                             band_inf_index = break_points[i][0],
                                             band_sup_index =  break_points[i][1],
                                             hash_fun = hash_functions_list[i])
    
    return bucket_ids_list

def ConvertAllPairsDictToPdDataframe(all_pairs_dict: dict,
                                     shared_bucket_threshold: int = 1,
                                     doc1_col_name: str = "doc1",
                                     doc2_col_name: str = "doc2",
                                     shared_bucket_number_col_name: str = "shared_bucket"):
    '''Given a dictionary with document pairs as key and number of shared bucket as value
    return a correspondent pandas dataframe filtering the pairs with shared bucket value
    greater than the specified threshold

    Args:
        all_pairs_dict (dict): with
                key = (doc1_id, doc2_id) (NOTE: to avoid duplicates doc1_id < doc2_id)
                value = number of shared buckets
        shared_bucket_threshold (int): pick only pairs with shared buckets number greater than this threshold

    Return:
        pd dataframe
    '''
    pass


# ---------------- LSH bands Lists data structure ------------------- # 

# --------- LSH one band buckets Lists data structure --------------- # 
class LSHOneBandBucketLists:
    
    def __init__(self, n_buckets: int):
        '''Data structure for a single band, each band is made of n_buckets buckets,
        a band of buckets is implemented as a list of lists (initialized as None objects).
        An index (set) is made where all bucket indexes with more than one element are kept.
        Args:
            - n_buckets (int): number of buckets
        '''
        self.band = [None for i in range(n_buckets)]
        self.more_than_one_index = set()
    
    def AddToBucket(self, bucket_id: int, object) -> None:
        '''
        Args:
            - bucket_id (int): id of the bucket where the object has to be placed
            - object (str): object to be place in the bucket, usually a document id
        '''
        if self.band[bucket_id] == None:
            self.band[bucket_id] = [object]
        else:
            self.band[bucket_id].append(object)
            # update index
            self.more_than_one_index.add(bucket_id)
    
    def __str__(self):
        return(f'''LSH BAND with {len(self.band)} buckets and {len(self.more_than_one_index)} buckets with more than one elements''')


# Used
# --------- LSH many bands buckets Lists data structure --------------- # 

class LSHManyBandsBucketLists:
    
    def __init__(self,
                 n_bands: int,
                 n_buckets: int,
                 signature_len: int,
                 hash_function_list: list):
        '''Data structure to store many bands, each band is made of n_buckets buckets,
        A list of LSHOneBandBucketLists is made.
        Args:
            - n_bands (int): number of bands
            - n_buckets (int): number of buckets
            - signature_len (int): length of the signature to be hashed
            - hash_function_list (list): list of hash function, one for each band
        '''
        self.bands_list = [LSHOneBandBucketLists(n_buckets = n_buckets) for i in range(n_bands)]
        self.signature_len = signature_len
        self.break_points = GenerateBreakPoints(n = signature_len, n_bands = n_bands)
        self.hash_function_list = hash_function_list
        
        if n_bands != len(hash_function_list):
            print(f"Warning: n_bands = {n_bands} != {len(hash_function_list)} = len(hash_function_list)")

    def AddToBands(self, bucket_ids: list, object):
        '''Add object to a bucket for each band.
        
        Args: 
            - bucket_ids (list of int): list of bucket ids ordered in the same way as the bands
            - object (str): object to be placed in the bucket, usually a document id
        '''
        # check 
        if len(bucket_ids) != len(self.bands_list):
            print("Warning: number of bucket ids different from band number! Returning None")
            return(None)
        else:
            for i in range(len(bucket_ids)):
                self.bands_list[i].AddToBucket(bucket_id = bucket_ids[i], object= object)
    
    def AddIdBySignature(self,
                         id,
                         signature):
        '''Add id in different buckets in different bands based on signature hash.
        Args: 
            - id: document id
            - signature: document signature
        '''
        self.AddToBands(bucket_ids = ComputeAllHashBands(signature = signature,
                                                                    break_points = self.break_points,
                                                                    hash_functions_list = self.hash_function_list),
                                                                    object = id)
    
    def AddIter(self,
                iterator):
        '''Add each element from the iterator to the LSH band buckets.
        Args:
            - iterator (iter): assuming each iteration gives the tuple (id, signature)
        '''
        for row in iterator:
                    self.AddIdBySignature(id = row[0], signature = row[1])
    
    
    def FindAllPairs(self) -> dict:
        '''Assuming the LSH has all documents:
        find all pairs of documents
        along with the number of shared buckets
        
        Return:
            dictionary (dict): with
                key = (doc1_id, doc2_id) (NOTE: to avoid duplicates doc1_id < doc2_id)
                value = number of shared buckets
        '''
        temp_all_combinations = defaultdict(lambda: 0)  # 0 (shared buckets)

        print("[INFO] Starting to process LSH bands...")

        for band_index, band_object in enumerate(self.bands_list):
            print(f"[DEBUG] Processing band {band_index + 1}/{len(self.bands_list)}...")
            # visit only buckets with more than one elements
            for k in band_object.more_than_one_index:
                # Generate unique pairs using combinations
                for doc_id1, doc_id2 in combinations(band_object.band[k], 2):  # Add to the visited set
                    temp_key = (doc_id1, doc_id2) if doc_id1 < doc_id2 else (doc_id2, doc_id1)
                    temp_all_combinations[temp_key][1] += 1  # Increment shared bucket count
        
        return temp_all_combinations
    
    def __str__(self):
        return(f'''LSH BAND with {len(self.bands_list)} bands each with {len(self.bands_list[0])} buckets''')


# NOT used
# ---------------- LSH bands BTree data structure ------------------- # 

# NOTE: this still needs to be completed, after the SQL class is completed
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
    

# NOT USED
# ---------------- LSH bands SQL data structure ------------------- # 

# option 1
# ------------- LSH one band: SQL TABLE(id_bucket, id_doc) --------#

class LSHOneBandSQLite_id_bucket_id_doc(sqlite_one_table.SQLiteOneTableGeneral):
    '''Conditional to one band, write the table TABLE(id_bucket, id_doc), 
    also create an index on id_bucket.
    The table will be used to find all id_docs with the same id_bucket value.
    '''
    
    def __init__(self,
                 col_types_list: list = ["INTEGER", "INTEGER"],
                 table_name: str = "table_1",
                 database_name: str = "db_name"):
        
        super().__init__(col_names_list = ["id_bucket", "id_doc"],
                         col_types_list = col_types_list,
                         col_do_pickle_bool_list = [False, False],
                         col_not_null_bool_list = [False, False],
                         col_is_unique_bool_list = [False, True],
                         col_create_index_bool_list = [True, False],
                         table_name = table_name,
                         database_name = database_name)

    # rename methods
    def insert_bucket_doc_pair(self,
                                 bucket_value,
                                 id_doc_value):
        
        super().insert_record_values(values_list = [bucket_value, id_doc_value])
    
    # this will manly will used for debug
    # to finish
    def getDocIdsByBucketDebugFetch(self,
                          output_path: str):
        ''' Method to get all document ids in the same bucket
        (only for buckets with more than one document,
        i.e. bucket id values that compare at least twice)
        
        NOTE: each output row follows the pattern id_bucket_value1|id_doc_value1,id_doc_value2,..
        so in order to extract the id_doc_values each row has to parsed.
        
        Args:
            - self
            - output_path: path where to store the result (can be a .txt file)
        
        Return: 
        '''
        # change output
        subprocess.call(["sqlite3", self.database_name,
                         f".output {output_path}"])
        
        # execute query
        self.connect.execute(f'''SELECT {self.col_names_list[0]},
                                GROUP_CONCAT({self.col_names_list[1]}) AS ids_doc
                                FROM {self.table_name}
                                GROUP BY {self.col_names_list[0]}
                                HAVING COUNT({self.col_names_list[0]}) >= 2;
                             ''')
        
        # restore default ouptut
        subprocess.call(["sqlite3", self.database_name,
                         ".output stdout"])
    
    def getDocIdsByBucket(self,
                          output_path: str):
        ''' Method to get all document ids in the same bucket
        (only for buckets with more than one document,
        i.e. bucket id values that compare at least twice)
        
        NOTE: each output row follows the pattern id_bucket_value1|id_doc_value1,id_doc_value2,..
        so in order to extract the id_doc_values each row has to parsed.
        
        Args:
            - self
            - output_path: path where to store the result (can be a .txt file)
        '''
        # change output
        subprocess.call(["sqlite3", self.database_name,
                         f".output {output_path}"])
        
        # execute query
        self.connect.execute(f'''SELECT {self.col_names_list[0]},
                                GROUP_CONCAT({self.col_names_list[1]}) AS ids_doc
                                FROM {self.table_name}
                                GROUP BY {self.col_names_list[0]}
                                HAVING COUNT({self.col_names_list[0]}) >= 2;
                             ''')
        
        # restore default ouptut
        subprocess.call(["sqlite3", self.database_name,
                         ".output stdout"])
