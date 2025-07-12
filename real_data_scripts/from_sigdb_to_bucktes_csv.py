# used to convert database.db to hadoop readable file system 

# Inputs: -----------------
# 1) database.db with record
# key = document id, value = (pickled np.array) signature
# 2) LSH parameters: number of bands, number of bucktes
# hash function for each band
# Produces ------------------
# file.csv with each row is a document
# first column is document 1
# all other columns are bucket ids
# Example --------------------------
# number of bands = 2, number of buckets per band = 3
# id_doc1, band1_bucket_id, band2_bucket_id
import pickle
import sqlite3
import numpy as np

from near_duplicate_doc_lsh.project.src import minhash as mh
from near_duplicate_doc_lsh.project.src import lsh
from near_duplicate_doc_lsh.real_data_scripts.lsh_all import LoadLshParamsFile as LLPF

# first we assume we know signature length
SIGNATURE_LENGTH = 100
# in future we will read it from the input
# (it's just the length of the signature np.array)

in_file_name = "test.db"
out_file_name = "out.csv"


# read metadata to get signature length
metadata_dict = ut.LoadMetadata(ut.JoinPaths(signature_folder_path,
                                             pm.METADATA_FILE_NAME))
                    
signature_len = metadata_dict[pm.MINHASH_METADATA_PARAMS_NAME][pm.SIGNATURE_LEN_FIELD_NAME]

n_documents = int(metadata_dict[pm.COLLECTION_PARAMS_NAME][pm.ORIGINAL_DOC_NUMBER_NAME]) + int(metadata_dict[pm.COLLECTION_PARAMS_NAME][pm.DUPLICATES_DOC_NUMBER_NAME])
n_buckets = times_buckets * n_documents
# Iterates over all signature database rows
# populate LSH band data structure

# generate hash functions for lsh bands hashing ----------------------
my_lsh_hash_fun_list = lsh.GenerateMotwaniHashFunctionsList(n_hash_functions = n_bands,
                                                                            band_size = signature_len // n_bands,
                                                                            modulo = n_buckets,
                                                                            seed = pm.SEED_LSH)

my_break_points = lsh.GenerateBreakPoints(n = signature_len,
                                                        n_bands = n_bands)

# open database connection
SigSQL = mh.SignaturesSQLite(database_name = signature_db_path)


# define rows iterator
fetched_rows_iterator = SigSQL.fetch_all_rows()


SigSQL.close_database()