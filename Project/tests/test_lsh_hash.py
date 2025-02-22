from src import lsh
from src import hashing
import unittest
import numpy as np



INT_TYPE = np.int16

def HashFunction1(number):
    return number % 3
def HashFunction2(number):
    return number % 4
def HashFunction3(number):
    return number % 5

# trivial hash function to use 

def HashFunctionSum(int_array: np.array):
    '''Sum the HashFunction1 of all array elements
    Args:
        - int_array : numpy array made of integers
        
    Return:
        - sum of hashes % 3 of the array's elements
    '''
    tot = 0
    
    for el in int_array:
        tot += el
    
    return tot

my_hash_fun_list = [HashFunctionSum, HashFunctionSum, HashFunctionSum]


def HashFunctionSum1(int_array: np.array):
    '''Sum the HashFunction1 of all array elements
    Args:
        - int_array : numpy array made of integers
        
    Return:
        - sum of hashes % 3 of the array's elements
    '''
    tot = 0
    
    for el in int_array:
        tot += HashFunction1(el)
    
    return tot

# input vector:
SIGNATURE1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype = INT_TYPE)

# first using the all signature as hashable
# hash parameters vector: (dimension hash to match with that of SIGNATURE1)
HASH_PARAM_VECTOR1 = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1], dtype = INT_TYPE)

# now 
HASH_PARAM_VECTOR2 = np.array([1, 1, 1], dtype = INT_TYPE)

MODULO1 = 2**32

# define the actual hash function
def MotwaniHash1(signature):
    return (hashing.MotwaniBandArrayHash(v = signature,
                                 random_int_array = HASH_PARAM_VECTOR1,
                                 modulo = MODULO1))



# given a vector of parameters [a1,...,a]


class TestLSHFunctions(unittest.TestCase):
    
    def test_ComputeOneHashGivenParameters(self):
        result1 = MotwaniHash1(SIGNATURE1)
        expected1 = sum(SIGNATURE1)
        
        self.assertEqual(result1, expected1)
        
        print("-----------------------------------------------")
        print("\n")
        
        
    
    def test_ComputeHashBand(self):
        signature1 = SIGNATURE1
        inf_index = 2
        sup_index = 5
        
        
        # trivial hash function
        # hash function used: HashFunction1
        expected1 = 0 + 1 + 2
        
        result1 = lsh.ComputeHashBand(signature1,
                                     inf_index,
                                     sup_index,
                                     HashFunctionSum1)
        self.assertEqual(result1, expected1)
        
        print("-----------------------------------------------")
        print("\n")
        
        # I need to define another hash function suited for the band dimension
        # non trivial hash function (base function is tested in test_ComputeOneHashGivenParameters)
        def MotwaniHash2(signature):
            return (hashing.MotwaniBandArrayHash(v = signature,
                                 random_int_array = HASH_PARAM_VECTOR1[inf_index:sup_index],
                                 modulo = MODULO1))
        
        result2 = lsh.ComputeHashBand(signature1,
                                     inf_index,
                                     sup_index,
                                     MotwaniHash2)
        
        
        expected2 = sum(signature1[inf_index:sup_index]) % MODULO1
        
        self.assertEqual(result2, expected2)
    
    def test_GenerateMotwaniHashFunctionsList(self):
        print("GenerateMotwaniHashFunctionsList test")
        
        l1 = lsh.GenerateMotwaniHashFunctionsList(n_hash_functions = 5,
                                                band_size = 3,
                                                modulo = 2**32,
                                                seed = 123)
        
        print("function list")
        print(l1)
        
        print("try one function, this should work")
        print(l1[0](np.array([1,1,2])))
        
        # print("try one function, this should give dimension error")
        # print(l1[0](np.array([1,1,2, 1])))
        
        
        print("-----------------------------------------------")
        print("\n")
    
    def test_ComputeAllHashBands(self):
        my_break_points = lsh.GenerateBreakPoints(n = len(SIGNATURE1),
                                                  n_bands = 3)
        
        print("my_break_points")
        print(my_break_points)
        print("\n")
        
        my_hash_bands = lsh.ComputeAllHashBands(signature = SIGNATURE1,
                                break_points = my_break_points,
                                hash_functions_list = my_hash_fun_list)
        
        print("my_hash_bands")
        print(my_hash_bands)
        

# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_lsh_hash

if __name__ == "__main__":
    unittest.main()