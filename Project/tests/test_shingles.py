from src import functions as funs

def Simple_Hash(object):
    return hash(object) % 30

# ---------------- Array Shingles ----------------#
def Test_TextToShinglesArray():
    w1 = "abcdefg"
    t1 = funs.TextToShinglesArray(w1, 3, Simple_Hash)
    print(t1)

# ------------ Set Shingles ---------------# 
def Test_TextToShinglesSet():
    w1 = "abcdefg"
    t1 = funs.TextToShinglesSet(w1, 3, Simple_Hash)
    print(t1)

# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m tests.test_shingles 

if __name__ == "__main__":
    # -------- Array Shingles ------------#
    Test_TextToShinglesArray() # ok
    # -------- Set Shingles --------------#
    Test_TextToShinglesSet() # ok