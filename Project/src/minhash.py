import numpy as np
import numba
from typing import Callable
from BTrees._LOBTree import LOBTree
import sqlite3
import pickle

#------------------ Generate Signature ---------------------#
@numba.njit
def NumbaSignatureByRow(shingles_array: np.array,
                              hash_params_matrix: np.array,
                              hash_fun: Callable,
                              int_type: np.uint32) -> np.array:
    '''Computes signature array.
    
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
                    the paramters of this function and those of 
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
    '''Computes signature array.
    
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
                    the paramters of this function and those of 
                    the hash_function
        int_type: integer type of the signature elements
        
    Returns:
        signature_array: the signatures contains the hashed positions instead 
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
    '''Compare two signatures element by element and  return the similarity
    
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
    # max number of childern an interior node could have
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
class SignaturesSQLite:
    '''Compute signatures, pickle them, save database and eventually unpickle by key.
    The database created assumes a simple schema:
    a unique table with fields: [id , pickled_signature (blob)]
    '''

    def __init__(self,
                 database_name: str,
                 id_type: str,
                 num_transaction_operations: int) -> None:
        '''Inizialize the instance creating the database
        
        Args:
            database_name: name of the database used or to be created
            id_type: type of id (used as database key)
            num_transaction_operation: number of operations before
                                        a database transaction is closed.
        '''
        
        # connect or create database
        self.db = sqlite3.connect(database_name)
        # cursor: used to perform operations
        self.cursor = self.db.cursor()
        
        # create table if not present
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS table
                            (id {id_type} PRIMARY KEY, signature blob)''')
        
        self.num_transaction_operations = num_transaction_operations
    
    def begin_transaction(self):
        '''Begin a transaction relative to the database.
        Remember to always end it.
        '''
        self.cursor.execute('BEGIN TRANSACTION')
        
    def end_transaction(self):
        '''Ending a database transaction.
        '''
        self.db.commit()
    
    def insert_id_signature(self,
                            id: int,
                            signature: np.array):
        '''Insert a pair (id, pickled_signature) in the database.
        The signature is pickled inside this function.
        
        NOTE:
        the insertion has to be done while in a transaction.
        
        Args:
            id: id of the document
            signature: signature relative to the document
        '''
        self.db.execute("INSERT INTO table VALUES (?,?)",
                  (id, pickle.dumps(signature)))
    
    def get_signature(self,
                      id: int) -> np.array:
        '''Return signature relative to id.
        
        Args:
            id: document id
        
        Return:
            signature: signature associated with the searched id
        '''
        self.db.execute("SELECT value FROM my_table WHERE id=?", (id,))
        return(pickle.loads(self.cursor.fetchone[0]))