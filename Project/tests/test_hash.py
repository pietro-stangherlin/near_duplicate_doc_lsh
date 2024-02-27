from src import hashing as hs
import unittest
import numpy as np


INT_TYPE_32 = np.int32
INT_TYPE_64 = np.int64
INT_TYPE_U64 = np.uint64

class TestHash(unittest.TestCase):

    def test_GenerateTwoUns64(self):
        num_tuples = 2
        seed = 123
        result = hs.GenerateTwoUns64(num_tuples, seed)
        print(f'''GenerateTwoUns64 with num_tuples {num_tuples} and seed {seed}:
               {result}''')
        print(f"result type: {type(result)}")

    def test_HashMultShift32(self):
        x = 914636142
        aux_params_1 = (3624216819017203054, 4184670734919783523)
        result = hs.HashMultShift32(x, aux_params_1)
        print(f'''HashMultiShift32(x = {x}, aux_params = {aux_params_1}) = 
              {result}''')



# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_hash

if __name__ == "__main__":
    unittest.main()