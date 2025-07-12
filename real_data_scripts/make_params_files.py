import json
import numpy as np
import importlib
import argparse

from near_duplicate_doc_lsh.project.src import hashing

# This just creates json files, each with shingle and minhash parameters
# which are saved in the minhash_params folder
# same for lsh parameters

# instructions:
# execute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts.make_params_files --collection arxiv

# MinHash function -----------------------------------------------------------
def SaveMinhashParamsFiles(shingle_lenghts,
                           signature_lengths,
                           hash_dict,
                           save_folder_minhash,
                           shingle_len_field_name,
                           shingle_hash__fun_field_name,
                           signature_len_field_name,
                           minhash_hash_fun_field_name,
                           minhash_bit_type_field_name,
                           minhash_hash_param_matrix_field_name,
                           seed_minhash):
    for bit_type in hash_dict:
        
        for shingle_len in shingle_lenghts:
            for signa_len in signature_lengths:
                parameters = {
        shingle_len_field_name: shingle_len,
        shingle_hash__fun_field_name: hash_dict[bit_type][0], # store hash function name
        signature_len_field_name: signa_len,
        minhash_hash_fun_field_name: hash_dict[bit_type][1], # store hash function name
        minhash_bit_type_field_name: bit_type,
        minhash_hash_param_matrix_field_name: hashing.GenerateNumpyArray(num_rows = signa_len,
                                                         num_cols =  2,
                                                         seed= seed_minhash,
                                                         reshape = True,
                                                         int_type = np.uint64).tolist()  # Convert the matrix to a list
    }

                # define the filename based on the signature length
                # add bit number
                filename = save_folder_minhash + f"minhash_par_shl_{shingle_len}_sil_{signa_len}_bit_{bit_type}.json"

                # save parameters to a file
                with open(filename, 'w') as file:
                    json.dump(parameters, file, indent = 4)


# LSH function -----------------------------------------------------
def SaveLSHParamsFiles(bands_numbers,
                       bucket_numbers,
                       save_folder_lsh,
                       bands_number_field_name,
                       buckets_number_field_name):

    for band_n in bands_numbers:
        for bucket_n in bucket_numbers:
            parameters = {
        bands_number_field_name: band_n,
        buckets_number_field_name: bucket_n}

            # define the filename based on the signature length
            # add bit number
            filename = save_folder_lsh + f"lsh_par_band_{band_n}_bucket_{bucket_n}.json"

            # save parameters to a file
            with open(filename, 'w') as file:
                json.dump(parameters, file, indent = 4)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
    "--collection",
    type=str,
    required=True,
    help="collection name (e.g. 'arxiv', 'robust')"
    )
    args = parser.parse_args()

    # Import the parameters module
    pm = importlib.import_module(f"near_duplicate_doc_lsh.real_data_scripts.{args.collection}.params.parameters")

    SaveMinhashParamsFiles(shingle_lenghts = pm.SHINGLE_LENGTHS,
                           signature_lengths = pm.SIGNATURE_LENGTHS,
                           hash_dict = pm.MINHASH_HASH_DICT,
                           save_folder_minhash = pm.MINHASH_PARAMS_FOLDER,
                           shingle_len_field_name = pm.SHINGLE_LEN_FIELD_NAME,
                           shingle_hash__fun_field_name = pm.SHINGLE_HASH_FUN_FIELD_NAME,
                           signature_len_field_name = pm.SIGNATURE_LEN_FIELD_NAME,
                           minhash_hash_fun_field_name = pm.MINHASH_HASH_FUN_FIELD_NAME,
                           minhash_bit_type_field_name = pm.MINHASH_BIT_TYPE_FIELD_NAME,
                           minhash_hash_param_matrix_field_name = pm.MINHASH_HASH_PARAM_MATRIX_FIELD_NAME,
                           seed_minhash = pm.SEED_MINHASH)
    
    SaveLSHParamsFiles(bands_numbers = pm.BANDS_NUMBERS,
                       bucket_numbers = pm.BUCKET_NUMBERS,
                       save_folder_lsh = pm.LSH_PARAMS_FOLDER,
                       bands_number_field_name = pm.BANDS_NUMBER_FIELD_NAME,
                       buckets_number_field_name = pm.BUCKETS_NUMBER_FIELD_NAME)