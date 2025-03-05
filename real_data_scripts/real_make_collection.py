from near_duplicate_doc_lsh.data_creation.src import make_collection as mc
from near_duplicate_doc_lsh.real_data_scripts import real_make_collection_params as rmcp
import random

# to do
# idea: make it once for a set of parameters:
# so make a for cycle
# where for each cycle a new folder with data and metadata is saved

# first just try with no_noise_100k

# instructions:
# execute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts.real_make_collection

random.seed(123)

# uncomment to actually write the line below
temp_dict = rmcp.robust_only_clones_no_noise_100k

fun_names_list = [fun.__name__ for fun in temp_dict["functions_edit_list"]]
fun_params_list = temp_dict["functions_params_list"]

other_names_list = ["original_doc_number", "duplicates_number"]
other_params_list = [temp_dict["n_lines_in_file"], temp_dict["n_random_lines"]]


mc.WriteRandomLines(**temp_dict)
mc.WriteMetadataCollection(param_names_list = fun_names_list + other_names_list,
                           param_values_list = fun_params_list + other_params_list ,
                           file_out_path = rmcp.no_noise_100k_path + "metadata.json")
