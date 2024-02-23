from ..src import make_collection as mc
from ..src import make_col_params as pm
import random

random.seed(123)

mc.WriteRandomLines(**pm.first_50_dict_params_yes_original)

# from general folder
#  python -m near_duplicate_doc_lsh.data_creation.tests.test_make_collection