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

# NOTE: this still need to be completed, after the SQL class is completed
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

# option 1
# ------------- LSH one band: SQL TABLE(id_bucket, id_doc) --------#
class LSHOneBandSQLite_id_bucket_id_doc(sqlite_one_table.SQLiteOneTable):
    '''Conditional to one band, write the table TABLE(id_bucket, id_doc), 
    also create an index on  id_bucket.
    The table will be used to find all id_docs with the same id_bucket value.
    '''
    
    def __init__(self,
                 database_name: str = "lsh_one_band_db",
                 col1_type: str = "INTEGER",
                 col2_type: str = "INTEGER",
                 table_name: str = "table_1",
                 col1_name: str = "bucket",
                 col2_name: str = "id_doc",
                 do_pickle: bool = False,
                 create_index_on_col1: bool = True):
        
        super().__init__(database_name,
                         col1_type,
                         col2_type,
                         table_name,
                         col1_name,
                         col2_name,
                         do_pickle,
                         create_index_on_col1)

        # rename methods
    def insert_bucket_id_pair(self,
                                 bucket_value,
                                 id_doc_value):
        
        super().insert_col1_col2(col1_value = bucket_value,
                                 col2_value = id_doc_value)
    
    # not used 
    def get_id_by_bucket(self,
                            bucket_value):
        
        super().get_col2_by_col1(col1_value = bucket_value)
    
    
    def GetDocIdsByBucket(self,
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
        self.connect.execute(f".output {output_path}")
        
        # execute query
        self.connect.execute(f'''SELECT {self.col1_name},
                                GROUP_CONCAT({self.col2_name}) AS col2_values
                                FROM {self.table_name}
                                GROUP BY {self.col1_name}
                                HAVING COUNT({self.col1_name}) >= 2;
                             ''')
        
        # restore default ouptut
        self.connect.execute(f".output stdout")


class LSHOneBandSQLite_id_bucket_id_doc_general(sqlite_one_table.SQLiteOneTableGeneral):
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
