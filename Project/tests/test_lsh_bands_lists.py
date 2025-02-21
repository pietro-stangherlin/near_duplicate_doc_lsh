from src import lsh
from src import hashing
import unittest
import numpy as np

N_BUCKETS = 5
N_BANDS = 3

# each key is doc_id, value is a list with buckets ids for each band
# warning: the bucket ids are dependent
MY_DOCS_AND_BUCKETS = {"doc1": [0,1,2],
                       "doc2": [0,2,3],
                       "doc3": [4,4,3]}

class LSHBandList(unittest.TestCase):

    def test_many_bands(self):
        many_bands = lsh.LSHManyBandsBucketLists(n_bands = N_BANDS, n_buckets = N_BUCKETS)
        
        for key in MY_DOCS_AND_BUCKETS:
            many_bands.AddToBands(bucket_ids = MY_DOCS_AND_BUCKETS[key],
                                  object = key)
            
        for i in range(len(many_bands.bands_list)):
            print(many_bands.bands_list[i].band)
        
# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_lsh_bands_lists

if __name__ == "__main__":
    unittest.main()