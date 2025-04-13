from ..src import minhash
from ..src import shingling
from ..src import line_reading as lr

from itertools import combinations
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

import pickle
import regex as re
import numpy as np
import time

# this file holds macro function useful to the evaluation

def ToMatchFromIdAndSignature(my_match: str,
                              id_name: str,
                              content_name: str,
                              shingle_len: int,
                              shingle_hash_fun,
                              minhash_hash_param_matrix,
                              minhash_hash_fun,
                              minhash_int_type) -> tuple:
    '''Given a 'match' string and minHashing parameters return a pair(id, signature)
    Args:
        - my_match
        - id_name
        - content_name
        - shingle_len
        - shingle_hash_fun
        - minhash_hash_param_matrix
        - minhash_hash_fun
        - minhash_int_type
    Return:
        - tuple (tuple): (id, signature)
    '''
    tuple_id_content = lr.ToJsonLineRead(my_match = my_match,
                                        id_name = id_name,
                                        content_name = content_name)
                        
    shingle_temp = shingling.TextToShinglesUniques(
                text = tuple_id_content[1],
                shingle_len = shingle_len,
                hash_fun = shingle_hash_fun)
            
    signature_temp = minhash.NumbaSignatureByRowParallel(
                shingles_array = np.array(list(shingle_temp),
                                          dtype= minhash_int_type),
                hash_params_matrix = minhash_hash_param_matrix,
                hash_fun = minhash_hash_fun,
                int_type = minhash_int_type)
    
    return (tuple_id_content[0], signature_temp)


def MinHashPopulateSignatureSQL(file_in_full_path: str,
                                signature_db_full_path: str,
                                id_name: str,
                                content_name: str,
                                shingle_len: int,
                                shingle_hash_fun,
                                minhash_hash_param_matrix,
                                minhash_hash_fun,
                                minhash_int_type,
                                batch_size: int,
                                match_string: str = r'\{(.*)\}'):
    '''
    '''
    SigSQL = minhash.SignaturesSQLite(database_name = signature_db_full_path)

    SigSQL.begin_transaction()
    
    start = time.time()
    
    with open(file_in_full_path, 'r', encoding = "utf-8") as fin:
        insertion_counter = 0
        for line in fin:
            # Use regular expression to find the content inside the brackets
            match = re.search(match_string, line)
            if match:
                tuple_id_signature = ToMatchFromIdAndSignature(my_match = match,
                                                           id_name = id_name,
                                                           content_name = content_name,
                                                           shingle_len = shingle_len,
                                                           shingle_hash_fun = shingle_hash_fun,
                                                           minhash_hash_param_matrix = minhash_hash_param_matrix,
                                                           minhash_hash_fun = minhash_hash_fun,
                                                           minhash_int_type = minhash_int_type)

                # add key (doc id) value (signature) pair to the SignatureSQL
                if insertion_counter % batch_size == 0:
                    SigSQL.end_transaction()
                    SigSQL.begin_transaction()
                    stop = time.time()
                    print(f"[INFO]: batch_size {batch_size} in time {round(stop - start)}")
                    start = time.time()
            
                SigSQL.insert_id_signature_pair(id_value = tuple_id_signature[0],
                                            signature_value = tuple_id_signature[1])
                insertion_counter += 1
                    
    SigSQL.end_transaction()
    SigSQL.close_database()

def MinHashPopulateSignatureSQLBatch(file_in_full_path: str,
                                 signature_db_full_path: str,
                                 id_name: str,
                                 content_name: str,
                                 shingle_len: int,
                                 shingle_hash_fun,
                                 minhash_hash_param_matrix,
                                 minhash_hash_fun,
                                 minhash_int_type,
                                 batch_size: int,
                                 match_string: str = r'\{(.*)\}'):
    """
    Optimized function for populating a signature database using pre-allocated batches.
    Args:
        file_in_full_path: Path to the input file containing data.
        signature_db_full_path: Path to the SQLite database.
        id_name: Field name for document ID.
        content_name: Field name for content.
        shingle_len: Length of the shingles.
        shingle_hash_fun: Function to hash shingles.
        minhash_hash_param_matrix: MinHash hash parameters.
        minhash_hash_fun: MinHash function.
        minhash_int_type: Integer type for MinHash.
        batch_size: Fixed size for each batch.
        match_string: Regular expression pattern for extracting content.
    """
    # Open a connection to the database
    SigSQL = minhash.SignaturesSQLite(database_name=signature_db_full_path)

    # Start a transaction
    SigSQL.begin_transaction()

    # Pre-allocate batch storage
    batch = [None] * batch_size
    batch_index = 0  # Track the current index in the batch

    start = time.time()
    
    with open(file_in_full_path, 'r', encoding="utf-8") as fin:
        for line in fin:
            # Use regular expression to extract content inside brackets
            match = re.search(match_string, line)
            if match:
                tuple_id_signature = ToMatchFromIdAndSignature(
                    my_match=match,
                    id_name=id_name,
                    content_name=content_name,
                    shingle_len=shingle_len,
                    shingle_hash_fun=shingle_hash_fun,
                    minhash_hash_param_matrix=minhash_hash_param_matrix,
                    minhash_hash_fun=minhash_hash_fun,
                    minhash_int_type=minhash_int_type
                )
                
                # Add the (id, signature) tuple to the batch
                batch[batch_index] = (tuple_id_signature[0], tuple_id_signature[1])
                batch_index += 1

                # Check if the batch is full
                if batch_index == batch_size:
                    SigSQL.bulk_insert(batch)  # Bulk insert the batch into the database
                    SigSQL.end_transaction()  # Commit the transaction
                    SigSQL.begin_transaction()  # Start a new transaction
                    batch_index = 0  # Reset the batch index
                    
                    stop = time.time()
                    print(f"[INFO]: batch_size {batch_size} in time {round(stop - start)}")
                    start = time.time()

    # Insert any remaining records in the batch
    if batch_index > 0:
        SigSQL.bulk_insert(batch[:batch_index])  # Handle the final partial batch

    # Commit the transaction and close the database
    SigSQL.end_transaction()
    SigSQL.close_database()


def process_line(line, match_string, id_name, content_name, shingle_len, shingle_hash_fun,
                 minhash_hash_param_matrix, minhash_hash_fun, minhash_int_type):
    """
    Process a single line to extract (id, signature) tuple.
    Args:
        - line: Line of text from the input file.
        - match_string: Regex pattern for matching.
        - id_name, content_name: Field names for document ID and content.
        - shingle_len, shingle_hash_fun, minhash_hash_param_matrix, minhash_hash_fun, minhash_int_type:
          Parameters for MinHash.
    Returns:
        - tuple: (id, signature) if matched, else None.
    """
    match = re.search(match_string, line)
    if match:
        return ToMatchFromIdAndSignature(
            my_match=match,
            id_name=id_name,
            content_name=content_name,
            shingle_len=shingle_len,
            shingle_hash_fun=shingle_hash_fun,
            minhash_hash_param_matrix=minhash_hash_param_matrix,
            minhash_hash_fun=minhash_hash_fun,
            minhash_int_type=minhash_int_type
        )
    return None

def MinHashPopulateSignatureSQLParallel(
        file_in_full_path: str,
        signature_db_full_path: str,
        id_name: str,
        content_name: str,
        shingle_len: int,
        shingle_hash_fun,
        minhash_hash_param_matrix,
        minhash_hash_fun,
        minhash_int_type,
        batch_size: int,
        num_threads: int = 4,
        match_string: str = r'\{(.*)\}'
    ):
    """
    Function for populating a signature database using streaming batches and concurrency.
    Args:
        - file_in_full_path: Path to the input file.
        - signature_db_full_path: Path to the SQLite database.
        - id_name, content_name: Field names for document ID and content.
        - shingle_len: Length of shingles.
        - shingle_hash_fun: Function for hashing shingles.
        - minhash_hash_param_matrix, minhash_hash_fun, minhash_int_type: MinHash parameters.
        - batch_size: Number of insertions per batch.
        - num_threads: Number of threads for concurrency.
        - match_string: Regex pattern for matching.
    """

    def process_batch(batch):
        """Insert a batch into the database with transaction management."""
        SigSQL = minhash.SignaturesSQLite(database_name=signature_db_full_path)
        try:
            SigSQL.begin_transaction()
            SigSQL.bulk_insert(batch)
            SigSQL.end_transaction()
        finally:
            SigSQL.close_database()

    start = time.time()

    # Use ThreadPoolExecutor for concurrent database insertions
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        batch = []
        
        with open(file_in_full_path, 'r', encoding="utf-8") as fin:
            for line in fin:
                match = re.search(match_string, line)
                if match:
                    tuple_id_signature = ToMatchFromIdAndSignature(
                        my_match=match,
                        id_name=id_name,
                        content_name=content_name,
                        shingle_len=shingle_len,
                        shingle_hash_fun=shingle_hash_fun,
                        minhash_hash_param_matrix=minhash_hash_param_matrix,
                        minhash_hash_fun=minhash_hash_fun,
                        minhash_int_type=minhash_int_type
                    )
                    batch.append((tuple_id_signature[0], tuple_id_signature[1]))

                    if len(batch) == batch_size:
                        # Submit the batch for concurrent processing
                        futures.append(executor.submit(process_batch, batch))
                        batch = []  # Reset the batch
                    
                        # Optionally wait for some tasks to complete to limit memory usage
                        if len(futures) >= num_threads:
                            for future in futures:
                                future.result()
                            futures.clear()

                        stop = time.time()
                        print(f"[INFO]: Processed batch_size {batch_size} in time {round(stop - start)}")
                        start = time.time()

        # Process the final batch if it contains any records
        if batch:
            futures.append(executor.submit(process_batch, batch))
            batch = []

        # Wait for all remaining tasks to complete
        for future in futures:
            future.result()

    print("[INFO]: All batches processed.")







