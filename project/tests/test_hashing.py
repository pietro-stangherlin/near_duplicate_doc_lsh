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
    print("--------------------------------------------------")
    print("\n")

def test_MurmUns64Hash():
    print("MurmUns64Hash test")

    text = "abcbd"
    hs1 = hs.MurmUns64Hash(text)
    print(f"text: {text}, hash: {hs1}, type of hash is {type(hs1)}")
    
    text = "abcbf"
    hs1 = hs.MurmUns64Hash(text)
    print(f"text: {text}, hash: {hs1}, type of hash is {type(hs1)}")

    text = "efcbf"
    hs1 = hs.MurmUns64Hash(text)
    print(f"text: {text}, hash: {hs1}, type of hash is {type(hs1)}")
    print("--------------------------------------------------")
    print("\n")

def test_GenerateNumpyArray():
    print("GenerateNumpyArray test")

    SEED = 123


    array = hs.GenerateNumpyArray(10, 2, SEED)
    print("10 x 2 u64 int matrix")
    print(array)

    print("--------------------------------------------------")
    print("\n")

    array = hs.GenerateNumpyArray(10, 3, SEED, int_type= INT_TYPE_U32)
    print("10 x 3 u32 int matrix")
    print(array)

    print("--------------------------------------------------")
    print("\n")


def test_NaiveHashU32Params():
    print("NaiveHashU32Params test")

    hs1 = hs.NaiveHashU32Params(np.uint32(2991312383),
                                     np.uint64([12847588855871978862, 5278339153051796803]))
    print(f"input u32 bit, hash: {hs1}")
    print("--------------------------------------------------")
    print("\n")

    hs1 = hs.NaiveHashU32Params(np.uint64(12632878844557580402),
                                      np.uint64([12847588855871978862, 5278339153051796803]))
    print(f"input u64 bit, hash: {hs1}")
    print("--------------------------------------------------")
    print("\n")

# here I need to test eventual conflicts 
# based on numba input (see function definition)
# it works
def test_NumbaNaiveHashU32Params():
    print("NumbaNaiveHashU32Params test")

    hs1 = hs.NumbaNaiveHashU32Params(np.uint32(2991312383),
                                     np.uint64([12847588855871978862, 5278339153051796803]))
    print(f"input u32 bit, hash: {hs1}")
    print("--------------------------------------------------")
    print("\n")

    hs1 = hs.NumbaNaiveHashU32Params(np.uint64(12632878844557580402),
                                      np.uint64([12847588855871978862, 5278339153051796803]))
    print(f"input u64 bit, hash: {hs1}")
    print("--------------------------------------------------")
    print("\n")

def test_MotwaniBandArrayHash():
    print("MotwaniBandArrayHash test")
    
    # vector to be hashed
    vector = np.array([4294967290, 4294967295, 4, 4294967200], 
                      dtype = np.uint32)
    
    # params of the hash function ("random integers")
    random_ints = np.array([1, 2, 3, 4], 
                      dtype = np.uint32)
    
    # modulo
    modulo_2_to_32 = 2**32
    
    t = hs.MotwaniBandArrayHash(v = vector,
                                random_int_array = random_ints,
                                modulo = modulo_2_to_32)
    
    print(t)
    
    print("--------------------------------------------------")
    print("\n")

def test_GenerateOneMotwaniHash():
    print("GenerateOneMotwaniHash test")
    
    f1 = hs.GenerateOneMotwaniHash(params = np.array([1,2,3]),
                                    modulo = 2**32)
    
    t1 = f1(np.array([1,1,1]))
    
    print(t1)
    
    print("\n")
    
    f1 = hs.GenerateOneMotwaniHash(params = np.array([1,2,3]),
                                    modulo = 2**32)
    
    t1 = f1(np.array([1,2,1]))
    
    print(t1)
    
    print("--------------------------------------------------")
    print("\n")

def main():
    test_MurmUns32Hash()
    test_MurmUns64Hash()

    test_GenerateNumpyArray()
    
    test_NaiveHashU32Params()
    
    test_NumbaNaiveHashU32Params()
    
    test_MotwaniBandArrayHash()
    
    test_GenerateOneMotwaniHash()


# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m tests.test_hashing

if __name__ == "__main__":
    main()