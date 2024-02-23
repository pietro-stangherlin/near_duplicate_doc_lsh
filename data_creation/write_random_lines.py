import re
import json
import random
from typing import Callable

def IsJson(text: str) -> bool:
    '''Check if text is a valid json object.
    
    Args:
        - text: text to check
        
    Returns:
        - bool: True if text is a valid json object, else False
    '''
    
    try:
        json.load(text)
        return True
    except:
        ValueError

def AcceptAllStrings(text: str) -> bool:
    '''Return True for any input
    '''
    return True

def WriteRandomLines(file_in: str,
                     file_out: str,
                     n_random_lines: int,
                     is_valid_line_fun: Callable,
                     n_lines_in_file: int = None):
    '''Write a fixed number of lines from a file at random.
    
    Args:
        - file_in: name of input file
        - file_out: name of output file
        - n_random_lines: number of lines to write
        - is_valid_line_fun: function that checks if a line is valid
        - n_lines_in_file: number of lines in input file, if known
    
    Note: if n_lines_in_file is not given the program
    iterates over all lines to count them.
    
    Returns: 
        - None: writes on output file
    '''
    with open(file_in, "r") as fin, open(file_out, "w") as fout:
        if n_lines_in_file == None:
            # count
            n_lines_in_file = 0
            for line in fin:
                n_lines_in_file += 1
        
        
        indexes = random.sample(range(n_lines_in_file),
                                       n_random_lines)