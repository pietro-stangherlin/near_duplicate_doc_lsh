from src import hashing as hs
import unittest
import numpy as np


INT_TYPE_32 = np.int32
INT_TYPE_64 = np.int64
INT_TYPE_U64 = np.uint64



class TestHash(unittest.TestCase):

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