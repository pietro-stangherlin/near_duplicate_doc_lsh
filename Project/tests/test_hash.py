from src import hashing as hs
import numpy as np


INT_TYPE_32 = np.int32
INT_TYPE_U32 = np.uint32
INT_TYPE_64 = np.int64
INT_TYPE_U64 = np.uint64

# NOTE: due to the random nature of the code it's difficult 
# if not impossibile to use the unit test module


def test_MurmUns32Hash():
    print("MurmUns32Hash test")

    text = "abcbd"
    hs1 = hs.MurmUns32Hash(text)
    print(f"text: {text}, hash: {hs1}, type of hash is {type(hs1)}")
    
    text = "abcbf"
    hs1 = hs.MurmUns32Hash(text)
    print(f"text: {text}, hash: {hs1}, type of hash is {type(hs1)}")

    text = "efcbf"
    hs1 = hs.MurmUns32Hash(text)
    print(f"text: {text}, hash: {hs1}, type of hash is {type(hs1)}")

def main():
    test_MurmUns32Hash()
     


# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_hash

if __name__ == "__main__":
    main()