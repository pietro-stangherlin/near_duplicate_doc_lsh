from ..src import make_collection as mc
from ..src import make_col_params as pm
import random

random.seed(123)

# uncomment to actually write the line below
mc.WriteRandomLines(**pm.arxiv_yes_original_first_1000)

# from general folder
#  python -m near_duplicate_doc_lsh.data_creation.tests.test_make_collection