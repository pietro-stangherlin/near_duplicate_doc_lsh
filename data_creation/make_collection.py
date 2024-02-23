import json
import random
import re 
import randomNoise as rn
from typing import Callable


# given a dataset like
# {"id" = "...", "content": "...", "id2" : int}

def EditTextOCR(text : str, 
             error_params: list) -> str:
    '''Given some text return a modified version of it.
    (simulating OCR errors)
    
    Args:
        - text: text to be edited
        - error_params: list of floats each in range [0,1],
                        the order is relative to the description below
                        (example [0.1, 0.5, 0])
    
    The editing occurs in this order (same as params list):
    1) transpose words
    2) trasponse chars
    3) swap chars
    
    Returns: 
        - edited text
    '''
    text = rn.OcrTransposition(text, error_params[0])
    text = rn.TransposeChars(text, error_params[1])
    
    return rn.SimulateOcrErrors(text, error_params[2])

# To fix adding random noise functions
# and their parameters
# maybe it's better to return an iterator
def EditJsonLineOCR(line: str,
                 id2_last_index: int,
                 error_params_list: list) -> list:
    '''Edit line according to some criteria.
    Return dictionary with modified lines and updated id2_index
    
    Args: 
        - line: line to be edited
        - id2_last_index: last numerical index used for documents
        - error_params_list: list of list of parameters, 
                            the oder of elements in each sublist should 
                            match that in EditTextOCR function.
                            (example [[0.1, 0.5, 0], [0.3, 0.1, 0.8]])
    
    Returns
    '''
    baseline = json.loads(line)
    
    for change in error_params_list:
         
        
    
    return line



# robust2
# n_lines_in_file = 528154
def WriteRandomLines(file_in: str,
                     file_out_collection: str,
                     file_out_index: str,
                     n_random_lines: int,
                     edit_line_fun : Callable,
                     write_original_lines: bool = True,
                     n_lines_in_file: int = 528155,
                     id2_last_index: int =  528154):
    '''Write a fixed number of lines from a file at random.
    
    Updates id2 for newly created documents and adds id3,
    
    Args:
        - file_in: name of input file
        - file_out_collection: name of output file
        - file_out_index: name of dictionary like file: {id_new: id_original, ...} 
        - n_random_lines: number of lines to write
        - edit_line_fun : functions editing the line
        - write_original_lines: write also the file_in lines (default True)
        - n_lines_in_file: number of lines in input file, if known
    
    Note: if n_lines_in_file is not given the program
    iterates over all lines to count them.
    
    Returns: 
        - None: writes on output file
    '''
    with open(file_in, "r") as fin, open(file_out_collection, "w") as fout, open(file_out_index, "w") as fout_index:
        if n_lines_in_file == None:
            # count
            n_lines_in_file = 0
            for line in fin:
                n_lines_in_file += 1
        
        
        edit_indexes = set(random.sample(range(n_lines_in_file),
                                       n_random_lines))
        
        
        line_index = 0
        
        # we created the new dataset with id2 as
        # the line number in the file
        
        for line in fin:
            if write_original_lines:
                
                fout.write(line)
                
            if line_index in edit_indexes:
                
                
            line_index += 1