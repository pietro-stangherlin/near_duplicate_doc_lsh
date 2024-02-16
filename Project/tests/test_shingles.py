from src import functions as funs

def Simple_Hash(object):
    return hash(object) % 30

# ---------------- Array Shingles ----------------#
def Test_TextToShinglesArray_yesHash():
    w1 = "abcdefg"

    t1 = funs.TextToShinglesArray(w1, 3, Simple_Hash, do_hash= True)

    print(t1)

def Test_TextToShinglesArray_noHash():
    w1 = "abcdefg"

    t1 = funs.TextToShinglesArray(w1, 3, Simple_Hash, do_hash= False)

    print(t1)

# ------------ Set Shingles ---------------# 
def Test_TextToShinglesSet_yesHash():
    w1 = "abcdefg"

    t1 = funs.TextToShinglesSet(w1, 3, Simple_Hash, do_hash= True)

    print(t1)

def Test_TextToShinglesSet_noHash():
    w1 = "abcdefg"

    t1 = funs.TextToShinglesSet(w1, 3, Simple_Hash, do_hash= False)

    print(t1)


# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m tests.test_shingles.py  

if __name__ == "__main__":
    # -------- Array Shingles ------------#
    Test_TextToShinglesArray_noHash() # ok
    Test_TextToShinglesArray_yesHash() # ok

    # -------- Set Shingles --------------#
    Test_TextToShinglesSet_noHash() # ok
    Test_TextToShinglesSet_yesHash() # ok