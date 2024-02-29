from src import hashing as hs
import unittest
import numpy as np


INT_TYPE_32 = np.int32
INT_TYPE_64 = np.int64
INT_TYPE_U64 = np.uint64



class TestHash(unittest.TestCase):

    def test_GenerateTwoUns64(self):
        num_rows = 2
        num_cols = 5
        seed = 123
        result = hs.GenerateUns64(num_rows, num_cols, seed)
        print(f'''GenerateTwoUns64 with num_rows {num_rows}, num_cols {num_cols} and seed {seed}:
               {result}''')
        print(f"result type: {type(result)}")
    
    def test_Naive32UniversalHash(self):
        x = 914636142
        aux_params_1 = (3624216819017203054, 4184670734919783523)
        result = hs.Naive32UniversalHash(x, aux_params_1)
        print(f'''Naive32UniversalHash(x = {x}, aux_params = {aux_params_1}) = 
              {result}''')

    def test_CWtrick32to32(self):
        x = 914636142
        aux_params_1 = [13131141, 13141411, 5363636, 747747484, 858488463]
        result = hs.CWtrick32to32(x = x, aux_params= aux_params_1)
        print(f'''CWtrick32to32(x = {x}, aux_params = {aux_params_1}) = 
              {result}''')
    
    def test_CWtrick32to64(self):
        x = 914636142
        aux_params_1 = [13131141, 13141411, 5363636, 747747484, 858488463]
        result = hs.CWtrick32to64(x = x, aux_params= aux_params_1)
        print(f'''CWtrick32to32(x = {x}, aux_params = {aux_params_1}) = 
            {result}''')
     


# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_hash

if __name__ == "__main__":
    unittest.main()