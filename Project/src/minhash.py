import numpy as np
import numba
from typing import Callable
from BTrees._LOBTree import LOBTree
import sqlite3
import pickle
import os

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
class SignaturesSQLite:
    '''Compute signatures, pickle them, save database and eventually unpickle by key.
    The database created assumes a simple schema:
    a unique table with fields: [key , value]
    '''

    def __init__(self,
                 database_name: str = "signatures_db",
                 key_type: str = "INTEGER",
                 value_type: str = "BLOB",
                 table_name: str = "signatures_table",
                 key_name: str = "id",
                 value_name: str = "signature",
                 num_transaction_operations: int = 1) -> None:
        '''Inizialize the instance creating the database.
        
        Args:
            database_name: name of the database used or to be created
            key_type: type of the table's key (INTEGER, REAL, TEXT, BLOB)
            value_type: type of the table's value (INTEGER, REAL, TEXT, BLOB)
            table_name: 
            key_name:
            value_name:
            num_transaction_operation: number of operations before
                                        a database transaction is closed.
        '''

        self.database_name = database_name
        self.table_name = table_name

        self.key_type = key_type
        self.value_type = value_type

        self.key_name = key_name
        self.value_name = value_name

        # connect or create database
        self.connect = sqlite3.connect(self.database_name)
        # cursor: used to perform operations
        self.cursor = self.connect.cursor()
        
        # create table if not present
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name}
                            ({self.key_name} {key_type} PRIMARY KEY, {self.value_name} {self.value_type})''')
        
        self.num_transaction_operations = num_transaction_operations
    
    def begin_transaction(self):
        '''Begin a transaction relative to the database.
        Remember to always end it.
        '''
        self.cursor.execute('BEGIN TRANSACTION')
        
    def end_transaction(self):
        '''Ending a database transaction.
        '''
        self.connect.commit()
    
    def insert_key_value(self, key, value):
        '''Insert a pair (id, pickled_signature) in the database.
        The signature is pickled inside this function.
        
        NOTE:
        the insertion has to be done while in a transaction.
        
        Args:
            key: id of the document
            value: signature relative to the document
        '''
        self.connect.execute(f"INSERT INTO {self.table_name} VALUES (?,?)",
                  (key, pickle.dumps(value)))
    
    def get_value_by_key(self, key):
        '''Return value relative to a key.
        
        Args:
            key: document id
        
        Return:
            value: signature associated with the searched key (id)
        '''
        value = self.connect.execute(f"SELECT {self.value_name} FROM {self.table_name} WHERE {self.key_name}=?",
                                     (key,))
        return((pickle.loads(value.fetchone()[0])))
    
    # to be tested
    def clear_database(self):
        '''Clear the SQLite database table.
        '''
        self.cursor.execute(f"DELETE FROM {self.table_name}")
    
    def close_database(self):
        '''Close the SQLite database connection.
        '''
        self.connect.close()
    
    def delete_database(self,
                        ask_confirm: bool = True):
        '''Delete the SQLite database file.

        Args:
            ask_confirm: if True (default) ask the user a confirmation
        '''

        if ask_confirm:
            delete_yes = input("If you want to delete the database file digit Y, any other input wont delete it.\n")
            
            if delete_yes == "Y":
                os.remove(self.database_name)
        
        else:
            os.remove(self.database_name)

    def print_all_records(self):
        '''Print all records in the SQLite database.
        '''
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
