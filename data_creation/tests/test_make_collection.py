from ..src import make_collection as mc
from ..src import make_col_params as pm
import random

random.seed(123)

# uncomment to actually write the line below
mc.WriteRandomLines(**pm.arxiv_yes_original_first_1000_only_duplicates)
mc.WriteMetadataCollection()


# from near_duplicate_doc_lsh folder folder
#  python -m data_creation.tests.test_make_collection

# from external folder
#  python -m near_duplicate_doc_lsh.data_creation.tests.test_make_collection