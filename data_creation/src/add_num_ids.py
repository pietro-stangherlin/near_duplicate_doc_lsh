import sys
import json 
from typing import Callable

# convert all the ids to int and add a new id field
# to that field

def ConvertID(file_in: str,
              file_out: str,
              id_new_name: str) -> None:
    '''Write in file_out the lines of file_in with id_new added.
    
    Args: 
        - file_in:name of input file;
            each line of the file should be json like:
            {field1: "content",...}
        - file_out: output file name
        - id_new_name: name of the old id field name
    
    Returns:
        - none
    '''
    with open(file_in, "r", encoding="UTF8") as fin, open(file_out, "w") as fout:
        line_count = 1
        for line in fin:
            
            data = json.loads(line.strip())
            
            data[id_new_name] = line_count
            
            fout.write(json.dumps(data) + '\n')
            
            line_count += 1
            
            
            
# not used
def FromStrToIntConvert(text: str, other: int) -> int:
    '''Convert Text to int.
    
    For all character in the string: convert all characters in int through
    the ord() function
    
    Args:
        - text: text to be converted in int
        - other: unused parameter, it'useful for other functions
    Returns:
        - int: the converted int
    '''
    encoded_string = ''
    
    for i in range(len(text)):
        encoded_string += str(ord(text[i])) 
    
    return int(encoded_string)
