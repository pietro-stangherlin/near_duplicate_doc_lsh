from near_duplicate_doc_lsh.data_creation.src import make_collection as mc
from near_duplicate_doc_lsh.real_data_scripts_arxiv.params import real_make_collection_params as rmcp
from near_duplicate_doc_lsh.real_data_scripts_arxiv.params import parameters as pm
import random

# to do
# idea: make it once for a set of parameters:
# so make a for cycle
# where for each cycle a new folder with data and metadata is saved

# instructions:
# execute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts_arxiv.real_make_collection


for i in range(len(rmcp.all_config_list)):
    random.seed(123)
    
    config_dict = rmcp.all_config_list[i]

    fun_names_list = [fun.__name__ for fun in config_dict["functions_edit_list"]]
    fun_params_list = config_dict["functions_params_list"]

    other_names_list = ["original_doc_number", "duplicates_number"]
    other_params_list = [config_dict["n_lines_in_file"], config_dict["n_random_lines"]]


    mc.WriteRandomLines(**config_dict)
    mc.WriteMetadataCollection(param_names_list = fun_names_list + other_names_list,
                            param_values_list = fun_params_list + other_params_list ,
                            file_out_path = rmcp.all_config_path_list[i] + pm.METADATA_FILE_NAME)
