# parameters used in test all
import numpy as np

# Doc ----------------------------------------------------------
ID_NAME = "id2"
CONTENT_NAME = "content"

# MinHash -------------------------------------------------------
SHINGLE_LEN = 9 # shingle len
SIGNATURE_LEN = 50 # signature len -> number of hash functions
EL = 2 # number of random integers generated

NUM_SQL_INSERTIONS = 1000

# LSH -----------------------------------------------------------
N_BANDS = 5 # number of bands
N_BUCKETS = 10**6 # number of buckets in each band

INT_TYPE_32 = np.uint32
INT_TYPE_64 = np.uint64




# folders and files path ------------------------------------------------------

# NOTE: maybe the subfolder names' creation should be automated
# (not the file names as they need to be accessed in order to make the analysis)

# original file
file_name_original_only = "test_data\\arxiv_first_1000_id2.json"
file_name_duplicates_only = "test_data\\arxiv_duplicates\\arxiv_clones_1000_only_duplicates.json"

# signature db folder and path -------
signature_db_folder = "test_data\\arxiv_duplicates\\sig_config1"
signature_db_relative_path = "signature_db"

# shingle and MinHash metadata -------
original_collection_metadata_path = "test_data\\arxiv_duplicates\\metadata_arxiv_1000_only_duplicates.json"
metadata_minhash_relative_path = "metadata_minhash.json"

# signature similarity csv ------
signature_sim_folder_path = "test_data\\arxiv_duplicates\\sig_config1\\lsh1"
signature_sim_relative_path = "arxiv_clones_first_1000_signature_sim.csv"

# lsh metadata -----
metadata_lsh_relative_path = "metadata_lsh.json"

