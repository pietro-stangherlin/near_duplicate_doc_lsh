from ..src import make_collection as mc
from ..src import make_col_params as pm
import random

random.seed(123)

# uncomment to actually write the line below
temp_dict = pm.arxiv_1000_only_duplicates

mc.WriteRandomLines(**temp_dict)
mc.WriteMetadataCollection(param_names_list = [fun.__name__ for fun in temp_dict["functions_edit_list"]],
                           param_values_list = temp_dict["functions_params_list"],
                           file_out_path = ".\\test_data\\metadata_arxiv_1000_only_duplicates.json")


# from near_duplicate_doc_lsh folder folder
# python -m data_creation.tests.test_make_collection

# from external folder
# python -m near_duplicate_doc_lsh.data_creation.tests.test_make_collection