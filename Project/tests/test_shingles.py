from src import functions_shingles as funs

# ---------------- Array Shingles ----------------#
def Test_TextToShinglesArray():
    w1 = "abcdefg"
    t1 = funs.TextToShinglesArray(w1, 3, lambda x : hash(x) % 5)
    print(t1)

# ------------ Set Shingles ---------------# 
def Test_TextToShinglesSet():
    w1 = "abcdefg"
    t1 = funs.TextToShinglesSet(w1, 3, lambda x : hash(x) % 5)
    print(t1)

# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m tests.test_shingles 

if __name__ == "__main__":
    # -------- Array Shingles ------------#
    Test_TextToShinglesArray() # ok
    # -------- Set Shingles --------------#
    Test_TextToShinglesSet() # ok