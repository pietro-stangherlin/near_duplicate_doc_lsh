from src.shingling import TextToShinglesArray
import ijson
import sys 
from BTrees.IOBTree import IOBTree

# Important: in final version 
# options must be passed as arguments throught the command line
# at the moment we just pass the input (json) file


# This is a prototype of the final version

input_file_name = sys.argv[1]