from ..src import make_collection as mc
from ..src import make_col_params as pm
import random

random.seed(123)

# uncomment to actually write the line below
temp_dict = pm.arxiv_1000_only_duplicates

fun_names_list = [fun.__name__ for fun in temp_dict["functions_edit_list"]]
fun_params_list = temp_dict["functions_params_list"]

other_names_list = ["original_doc_number", "duplicates_number"]
other_params_list = [temp_dict["n_lines_in_file"], temp_dict["n_random_lines"]]


mc.WriteRandomLines(**temp_dict)
mc.WriteMetadataCollection(param_names_list = fun_names_list + other_names_list,
                           param_values_list = fun_params_list + other_params_list ,
                           file_out_path = "test_data\\arxiv_duplicates\\metadata_arxiv_1000_only_duplicates.json")


# from near_duplicate_doc_lsh folder folder
# python -m data_creation.tests.test_make_collection

# from external folder
# python -m near_duplicate_doc_lsh.data_creation.tests.test_make_collection