from near_duplicate_doc_lsh.data_creation.src import make_collection as mc
import random

import importlib
import argparse

# to do
# idea: make it once for a set of parameters:
# so make a for cycle
# where for each cycle a new folder with data and metadata is saved

# instructions:
# execute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts.real_make_collection --collection arxiv


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
rmcp = importlib.import_module(f"near_duplicate_doc_lsh.real_data_scripts.{args.collection}.params.real_make_collection_params")


for i in range(len(rmcp.all_config_list)):
    random.seed(123)
    
    config_dict = rmcp.all_config_list[i]

    fun_names_list = [fun.__name__ for fun in config_dict["functions_edit_list"]]
    fun_params_list = config_dict["functions_params_list"]

    other_names_list = [pm.ORIGINAL_DOC_NUMBER_NAME, pm.DUPLICATES_DOC_NUMBER_NAME]
    other_params_list = [config_dict["n_lines_in_file"], config_dict["n_random_lines"]]


    mc.WriteRandomLines(**config_dict)
    mc.WriteMetadataCollection(param_names_list = fun_names_list + other_names_list,
                            param_values_list = fun_params_list + other_params_list ,
                            file_out_path = rmcp.all_config_path_list[i] + pm.METADATA_FILE_NAME)
