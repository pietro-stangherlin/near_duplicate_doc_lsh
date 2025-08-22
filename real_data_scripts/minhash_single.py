
from near_duplicate_doc_lsh.project.src import macro
import argparse

import numpy as np
import os
import json

# change argument each time
if __name__ == "__main__":
    macro.MinHashPopulateSignatureSQL(file_in_full_path = pm.ORIGINAL_PATH,
                                    signature_db_full_path = signature_db_full_path,
                                    id_name = pm.ID_FIELD_NAME,
                                    content_name = pm.CONTENT_FIELD_NAME,
                                    shingle_len = par_dict[pm.SHINGLE_LEN_FIELD_NAME],
                                    shingle_hash_fun = par_dict[pm.SHINGLE_HASH_FUN_FIELD_NAME],
                                    minhash_hash_param_matrix = par_dict[pm.MINHASH_HASH_PARAM_MATRIX_FIELD_NAME],
                                    minhash_hash_fun = par_dict[pm.MINHASH_HASH_FUN_FIELD_NAME],
                                    minhash_int_type = bit_type,
                                    batch_size = pm.NUM_SQL_INSERTIONS,
                                    match_string = r'\{(.*)\}')