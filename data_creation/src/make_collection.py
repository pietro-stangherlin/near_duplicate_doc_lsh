import json
import random
import re
from . import randomNoise as rn
from typing import Callable

# given a dataset like
# {"id" = "...", "content": "...", "id2" : "int"}

def EditTextOCR(text : str,
                error_params: list) -> str:
    '''Given some text return a modified version of it.
    (simulating OCR errors)
    
    Args:
        - text: text to be edited
        - error_params: list of floats each in range [0,1],
                        the order is relative to the description below
                        (example [0.1, 0.5, 0])
    
    The editing occurs in this order (same as error_params list):
    1) transpose words
    2) trasponse chars
    3) swap chars
    
    Returns: 
        - edited text
        
    *NOTES: this function could be generalized accepting a list of functions
    along with a list of list of their parameters, for now we keep it simple
    '''
    text = rn.OcrTransposition(text, error_params[0])
    text = rn.TransposeChars(text, error_params[1])
    
    return rn.SimulateOcrErrors(text, error_params[2])


def EditDictOCR(dictionary: dict,
                id_int_unique_last_index: int, # id2 last value
                id_int_unique_field_name: str, # id2
                id_int_link_field_name: str, # id3
                content_field_name: str,
                error_params_list: list,
                edit_text_function: Callable,
                ) -> iter:
    '''Edit dictionary according to some criteria, produces an iterator of dictionaries made this way.
    
    Assuming there are k elements in error_params_list ->
    the iterator apply 
    
    Args: 
        - dictionary: dictionary to be edited
        - id_int_unique_last_index: last numerical index used for documents' id2
        - id_int_unique_field_name: name of id2 field
        - id_int_link_field_name: name of the new id field where the original
                                doc id_int_unique is written
        - content_field_name: name of the content (str) to be edited
        - error_params_list: list of list of parameters, 
                            the oder of elements in each sublist should 
                            match that in EditTextOCR function.
                            (example [[0.1, 0.5, 0], [0.3, 0.1, 0.8]])
        - edit_text_function: function to edit the text inside the dictionary["contend_field_name"]
                            it is assumed this functions parameters are:
                            (text_to_be_edited, list_of_other_functions_params)
    
    Yield:
        - edited dictionary
    
    NOTES: The indexing of edited dictionary works only with our way of creating the new ids,
    which assumes the maximum id of the collection is known
    so each new id is made by one increment of the maximum
    (this way we are sure each document has its unique id)
    '''
    
    original_id_unique = dictionary[id_int_unique_field_name]
    original_content = dictionary[content_field_name]
    
    # new numerical id2
    next_id_int = id_int_unique_last_index + 1
    
    for error_list in error_params_list:
        yield {id_int_unique_field_name: next_id_int,
               id_int_link_field_name: original_id_unique,
               content_field_name: edit_text_function(original_content, error_list)}
        next_id_int += 1


# robust2
# n_lines_in_file = 528154
def WriteRandomLines(file_in: str,
                     file_out_collection: str,
                     file_out_index: str,
                     n_random_lines: int,
                     edit_dict_fun : Callable,
                     id_int_unique_field_name: str,
                     id_int_link_field_name: str,
                     edit_text_function: Callable,
                     content_field_name: str,
                     error_params_list: list,
                     write_original_lines: bool = True,
                     n_lines_in_file: int = 528155, # robust docs number
                     id_int_unique_last_index: int =  528154): # robust docs number - 1
    '''Write a fixed number of lines from a file at random.
    
    Updates id_int_unique for newly created documents and adds id_int_link.
    Assume a file_in where each ROW has this structure:
    {"id_int_unique_field_name" = "...",
    "content_field_name": "..."}\n
    If it has more fields they'll be ignored
    
    Args:
        - file_in: name of input file
        - file_out_collection: name of output file
        - file_out_index: name index like file: 
                        id_int_unique_1,id_int__unique_original_1\nid_int_unique_2,id_int_unique_original_2
        - n_random_lines: number of lines to write
        - edit_line_fun: functions editing the dictionary corresponding to the json line
        - id_int_unique_field_name: name of id unique id made by integers
        - id_int_link_field_name: name of new id which get value None for original documents,
                                for edited documents is used the value of id_int_unique of the
                                document from which they are derived
        - edit_text_function: functions actually used to edit the text
        - content_field_name: name of field where the actual text to edit is
        - error_params_list: list of lists of parameters: each sublist is the second
                            parameter of edit_text_function
        - write_original_lines: write also the file_in lines (default True)
        - n_lines_in_file: number of lines in input file, if known
        - id_int_unique_last_index: maximum int index in the collection,
                                    needed to make new unique indexes by incrementing it
    
    Note: if n_lines_in_file is not given the program
    iterates over all lines to count them.
    
    Returns: 
        - None: writes on output file
    '''
    with open(file_in, "r") as fin, open(file_out_collection, "w", encoding="utf-8") as fout, open(file_out_index, "w") as fout_index:
        if n_lines_in_file == None:
            # count
            n_lines_in_file = 0
            for line in fin:
                n_lines_in_file += 1

        edit_indexes = set(random.sample(range(n_lines_in_file),
                                    n_random_lines))

        line_index = 0
        id_int_unique_last_index += 1
        
        # write index header
        fout_index.write("doc1_id,doc2_id\n")

        # create the new dataset with id2 as
        # the line number in the file

        for line in fin:
            # match = re.search(r"\{.*?\}", line)

            original_line_dict = json.loads(line.strip())

            if write_original_lines:
                original_line_dict[id_int_link_field_name] = "None"
                json.dump(original_line_dict, fout)  # use json.dump here
                fout.write("\n")  # add a newline after each json object

            if line_index in edit_indexes:
                
                for edited in edit_dict_fun(original_line_dict,
                                            id_int_unique_last_index,  # id2 last value
                                            id_int_unique_field_name,  # id2
                                            id_int_link_field_name,  # id3
                                            content_field_name,
                                            error_params_list,
                                            edit_text_function):

                    json.dump(edited, fout)  # use json.dump here
                    fout.write("\n")  # add a newline after each json object

                    # write the indexed in the index file
                    # first column: original file id
                    # second column: duplicate file id
                    fout_index.write(f"{original_line_dict[id_int_unique_field_name]},{id_int_unique_last_index}\n")
                    id_int_unique_last_index += 1

            line_index += 1
