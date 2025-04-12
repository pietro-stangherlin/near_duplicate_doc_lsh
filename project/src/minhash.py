import numpy as np
import pandas as pd
import numba
from typing import Callable
import pickle

from BTrees._LOBTree import LOBTree
from . import sqlite_one_table


#------------------ Generate Signature ---------------------#
@numba.njit
def NumbaSignatureByRow(shingles_array: np.array,
                        hash_params_matrix: np.array,
                        hash_fun: Callable,
                        int_type: np.uint32) -> np.array:
    '''Compute signature array.
    
    Args:
        shingles_array: numpy array of shingles (integers)
        hash_params_matrix: matrix of parameters (other than the hashable)
                            used to compute the hash function,
                            each row corresponds to a set of parameters
                            for a different hash function accepting
                            a number of auxiliary parameters equals to 
                            the columns number
        hash_fun: the hash function used, note that at the moment
                    is not implemented any compatibility check between
                    the parameters of this function and those of 
                    the hash_function
        int_type: integer type of the signature elements
        
    Returns:
        signature_array: contains the hashed positions instead 
                            of the values, this doesn't change the result 
                            as long as each shingle has the same type of 
                            its hash (ex. uint32 uint32) if the hash function
                            behaves decently, i.e. looks approximatley like
                            a bijective function
    '''
    num_matrix_rows = hash_params_matrix.shape[0]
    signature = np.full(shape = num_matrix_rows,
                        fill_value = np.iinfo(int_type).max,
                        dtype = int_type)
    
    
    for row_index in range(num_matrix_rows):
        for shingle in shingles_array:
            value = hash_fun(shingle, hash_params_matrix[row_index])
            if value < signature[row_index]:
                signature[row_index] = value
    
    return signature


@numba.njit(parallel = True)
def NumbaSignatureByRowParallel(shingles_array: np.array,
                              hash_params_matrix: np.array,
                              hash_fun: Callable,
                              int_type: np.uint32) -> np.array:
    '''Compute signature array.
    
    Args:
        shingles_array: numpy array of shingles (integers)
        hash_params_matrix: matrix of parameters (other than the hashable)
                            used to compute the hash function,
                            each row corresponds to a set of parameters
                            for a different hash function accepting
                            a number of auxiliary parameters equals to 
                            the columns number
        hash_fun: the hash function used, note that at the moment
                    is not implemented any compatibility check between
                    the parameters of this function and those of 
                    the hash_function
        int_type: integer type of the signature elements
        
    Returns:
        signature_array: the signatures contain the hashed positions instead 
                            of the values, this doesn't change the result 
                            as long as each shingle has the same type of 
                            its hash (ex. uint32 uint32) if the hash function
                            behaves decently, i.e. looks approximatley like
                            a bijective function
    '''
    num_matrix_rows = hash_params_matrix.shape[0]
    signature = np.full(shape = num_matrix_rows,
                        fill_value = np.iinfo(int_type).max,
                        dtype = int_type)
    
    # numba.range tries to parallelize the for loop
    for row_index in numba.prange(num_matrix_rows):
        for shingle in shingles_array:
            value = hash_fun(shingle, hash_params_matrix[row_index])
            if value < signature[row_index]:
                signature[row_index] = value
    
    return signature


# -------- Compare Signatures ---------
@numba.njit
def SignatureSimilarity(sig1: np.array, sig2: np.array) -> float:
    '''Compare two signatures element by element and return the similarity
    
    Args:
        sig1: signature 1 (array of len k)
        sig2: signature 2 (array of len k)
    
    Returns: 
        number positions with the same elements / total positions number
    '''
    if sig1.shape != sig2.shape:
        print("Error: signatures have different lengths")
        return 0.0

    equals = np.sum(sig1 == sig2)
    
    return equals / sig1.size

# Testing needed
def GetSignatureSimilarityArray(pairs_sharedbukets_pd: pd.DataFrame,
                                doc_signature_dict: dict,
                                doc1_col_name: str = "doc1",
                                doc2_col_name: str = "doc2") -> np.array:
    '''Given a pandas dataframe with document ids columns and a dictionary
    with key = doc_id and value = signature return a sorted (same order of pairs_sharedbukets_pd rows) array
    of signature similarities

    Args:
    - pairs_sharedbuckets_dict (dict): with
                key = (doc1_id, doc2_id) (NOTE: to avoid duplicates doc1_id < doc2_id)
                value = number of shared buckets
    - doc_signature_dict (dict): key = doc_id and value = signature
    - doc1_col_name (str)
    - doc2_col_name (str)

    Return:
        - numpy array (np.array): sorted (same order of pairs_sharedbukets_pd rows) array
    of signature similarities
    '''
    n_row = pairs_sharedbukets_pd.shape[0]
    signatures_similarities_np_array = np.zeros(n_row)

    # get doc1 and doc2 indexes
    doc1_index = pairs_sharedbukets_pd.columns.get_loc(doc1_col_name)
    doc2_index = pairs_sharedbukets_pd.columns.get_loc(doc2_col_name)

    for i, row in enumerate(pairs_sharedbukets_pd.itertuples(index=False)):
        if i % 10^6 == 0:
            print(f"[DEBUG] Processing similarity for pair {i}/{len(n_row)}...")

        # debug: 
        print(f"[DEBUG] row[doc1_index] = {row[doc1_index]}")
        print(f"[DEBUG] type(row[doc1_index]) = {type(row[doc1_index])}")

        print(f"[DEBUG] row[doc2_index] = {row[doc2_index]}")
        print(f"[DEBUG] type(row[doc2_index]) = {type(row[doc2_index])}")


        

        value1 = doc_signature_dict[row[doc1_index]]
        value2 = doc_signature_dict[row[doc2_index]]

        signatures_similarities_np_array[i] = SignatureSimilarity(value1, value2)
    
    return(signatures_similarities_np_array)

# NOT USED
# --------- Signatures set data structure ---------------
class SignaturesBTree(LOBTree):
    '''BTree used to store doc id as keys and doc signatures as values.
    
    Inherit the IOBTree class from BTrees module: 
    https://btrees.readthedocs.io/
    
    Args: 
        key (unsigned_integer): Unsigned integer (doc id)
        value (numpy_array): np.array of int (doc signature)
    '''
    # change if necessary
    # max number of elements a leaf can have
    max_leaf_size = 500
    # max number of children an interior node could have
    max_internal_size = 1000

    def compute_similarity(self, id1: int, id2: int) -> float:
        '''Compare the two documents' signatures returning the similarity
    
        Args:
            id1: document 1 id
            id2: document 2 id
    
        Returns:
            fraction (float): number positions with the same elements / total positions number
        '''
        return SignatureSimilarity(self[id1], self[id2])

# ---------------- Signatures on mass memory with SQLite ------------------------
class SignaturesSQLite(sqlite_one_table.SQLiteOneTable):
    '''Compute signatures, pickle them, save database and eventually unpickle by key.

    Inherits from the SQLiteOneTable class.
    '''
    def __init__(self, 
                 database_name: str = "signature_db",
                 col1_type: str = "INTEGER",
                 col2_type: str = "BLOB",
                 table_name: str = "table_1",
                 col1_name: str = "id_doc",
                 col2_name: str = "signature",
                 do_pickle: bool = True,
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
    def insert_id_signature_pair(self,
                                 id_value,
                                 signature_value):
        
        super().insert_col1_col2(col1_value = id_value,
                                 col2_value = signature_value)
    
    def get_signature_by_id(self,
                            id_value):
        
        return(super().get_col2_by_col1(col1_value = id_value))
    
    # testing needed
    def fetch_rows_by_doc_ids(self,
                              doc_ids_batch):
        """
        Fetch rows from the database for the specified document IDs.
        Args:
            - doc_ids_batch: A batch of document IDs
        Returns:
            - List of rows corresponding to the specified document IDs, with unpickled values if needed.
        """
        placeholders = ','.join(['?'] * len(doc_ids_batch))  # Create placeholders for the query
        query = f"SELECT * FROM {self.table_name} WHERE {self.col1_name} IN ({placeholders})"
        self.cursor.execute(query, doc_ids_batch)
        rows = self.cursor.fetchall()

        # unpickle the values in column2 if requested
        if self.do_pickle:
            rows = [(row[0], pickle.loads(row[1])) for row in rows]

        return rows
    
    def GetDocSignatureSubsetDictionary(self,
                                        doc_ids_subset: np.array,
                                        batch_size: int) -> dict:
        '''Given an array of document id return a dictionary with key = doc_id, value = signature.

        Args: 
            - doc_ids_subset (np.array): array of document ids to fetch
            - batch_size (int): batch size for each iteration
        
        Return:
            - dictionary (dict): with key = doc_id, value = signatur for the document subset
        '''

        signature_cache = {}
        print("[INFO] Starting to preload document signatures...")
        for i in range(0, len(doc_ids_subset), batch_size):
            batch = doc_ids_subset[i:i + batch_size]
            print(f"[DEBUG] Fetching batch {i // batch_size + 1} containing {len(batch)} document IDs...")
            rows = self.fetch_rows_by_doc_ids(doc_ids_batch = batch)
            for row in rows:
                print(f"[DEBUG] row = {row}")
                signature_cache[row[0]] = row[1]  # row[0] = doc_id and row[1] is the signature
        
        print(f"[INFO] Finished preloading document signatures. Cached {len(signature_cache)} signatures.")
        return signature_cache
        

# NOT USED -> to USE
# here the MinHash class stores (as it should)
# the MinhasParameters making less error prone
class MinHashSQLite:
    
    def __init__(self,
                 minhash_hash_param_matrix,
                 minhash_hash_fun,
                 minhash_int_type,
                 **signature_sqlite_kwargs):
        
        # MinHashParameters
        self.minhash_hash_param_matrix = minhash_hash_param_matrix
        self.minhash_hash_fun = minhash_hash_fun
        self.minhash_int_type = minhash_int_type
        
        # signature instance
        self.signature_sql = SignaturesSQLite(**signature_sqlite_kwargs)
        