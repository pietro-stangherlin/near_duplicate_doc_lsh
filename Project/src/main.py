from src.shingling import TextToShinglesArray
import ijson
import sys 
from BTrees.IOBTree import IOBTree

# Important: in final version 
# options must be passed as arguments throught the command line
# at the moment we just pass the input (json) file


# This is a prototype of the final version

input_file_name = sys.argv[1]

# First we assume the minhash could be held in main memory (as a btree)
def LSH(filename, signatures):
    '''Execute LSH.
    '''
    with open(filename, 'r') as file:
        # create a new JSON object
        objects = ijson.items(file, 'item')
        for obj in objects:
            # process the JSON object
            id_temp = obj["id"]

            # generate shingles vector
            shingles_temp = TextToShinglesArray(obj["text"], 3,
                                lambda x: hash(x) % 10)
            
            # generate signature


        

if __name__ == "__main__":
    # allocate signatures btree
    signature_btree = IOBTree()

    LSH(input_file_name)

