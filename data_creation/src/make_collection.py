import json
import random
from . import randomNoise as rn
from typing import Callable

# given a dataset like
# {"id" = "...", "content": "...", "id2" : "int"}

ocr_functions_list = [rn.OcrTransposition, rn.TransposeChars, rn.SimulateOcrErrors]

def EditText(text : str,
                functions_params_list: list,
                functions_edit_list: list = ocr_functions_list) -> str:
    '''Given some text return a modified version of it.
    (simulating OCR errors)
    
    The editing occurs in the same order as error_params list
    
    Args:
        - text (str): text to be edited
        - functions_params_list (list): list of floats each in range [0,1],
                        the order is relative to the description below
                        (example [0.1, 0.5, 0])
        - functions_edit_list (list): list of editing functions, the order counts 
    
    Returns: 
        - edited text (str)
    '''
    if len(functions_edit_list) != len(functions_params_list):
        print("Error: length of functions list is different from associated error parameters list")
        return None

    for func, param in zip(functions_edit_list, functions_params_list):
        text = func(text, param)
    
    return text

def EditDict(dictionary: dict,
                id_int_unique_last_index: int, # id2 last value
                id_int_unique_field_name: str, # id2
                id_int_link_field_name: str, # id3
                content_field_name: str,
                functions_params_list: list,
                functions_edit_list: list = ocr_functions_list,
                ) -> dict:
    '''Edit dictionary according to some criteria, produces an iterator of dictionaries made this way.
    
    Assuming there are k elements in error_params_list ->
    the iterator apply 
    
    Args: 
        - dictionary: dictionary to be edited
        - id_int_unique_last_index (int): last numerical index used for documents' id2
        - id_int_unique_field_name (str): name of id2 field
        - id_int_link_field_name (str): name of the new id field where the original
                                doc id_int_unique is written
        - content_field_name (str): name of the content (str) to be edited
        - functions_params_list (list): list of list of parameters, 
                            the order of elements in each sublist should 
                            match the one of functions_edit_list
        - functions_edit_list (list): list of editing functions, the order counts
    
    Return:
        - edited dictionary
    
    NOTE: The indexing of edited dictionary works only with our way of creating the new ids,
    which assumes the maximum id of the collection is known
    so each new id is made by one increment of the maximum
    (this way we are sure each document has its unique id)
    '''
    
    original_id_unique = dictionary[id_int_unique_field_name]
    original_content = dictionary[content_field_name]
    
    return {id_int_unique_field_name: id_int_unique_last_index + 1,  # new numerical id
               id_int_link_field_name: original_id_unique,
               content_field_name: EditText(text = original_content,
                                               functions_params_list = functions_params_list,
                                               functions_edit_list = functions_edit_list)}


# robust2
# n_lines_in_file = 528154
def WriteRandomLines(file_in: str,
                     file_out_collection: str,
                     file_out_index: str,
                     n_random_lines: int,
                     id_int_unique_field_name: str,
                     id_int_link_field_name: str,
                     content_field_name: str,
                     functions_params_list: list,
                     functions_edit_list: list = ocr_functions_list,
                     write_original_lines: bool = True,
                     n_lines_in_file: int = None, # robust docs number
                     id_int_unique_last_index: int =  None): # robust docs number
    '''Write a fixed number of lines from a file at random.
    
    Updates id_int_unique for newly created documents and adds id_int_link.
    Assume a file_in where each ROW has this structure:
    {"id_int_unique_field_name" = "...",
    "content_field_name": "..."}\n
    If it has more fields they'll be ignored
    
    Args:
        - file_in (str): name of input file
        - file_out_collection (str): name of output file
        - file_out_index (str): name index like file: 
                        id_int_unique_1,id_int__unique_original_1\nid_int_unique_2,id_int_unique_original_2
        - n_random_lines (int): number of lines to write
        - id_int_unique_field_name (str): name of id unique id made by integers
        - id_int_link_field_name (str): name of new id which get value None for original documents;
                                for edited documents it is used the value of id_int_unique of the
                                document from which they are derived
        - content_field_name (str): name of field where the actual text to edit is
        - functions_params_list (list): list of lists of parameters: each sublist is the second
                            parameter of edit_text_function
        - write_original_lines (bool): write also the file_in lines (default True)
        - n_lines_in_file (int): number of lines in input file, if known
        - id_int_unique_last_index (int): maximum int index in the collection,
                                    needed to make new unique indexes by incrementing it
    
    NOTE: if n_lines_in_file is not given the program
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

        # index of ids (integers) of documents to be duplicated and edited
        edit_indexes = set(random.sample(range(1, n_lines_in_file + 1),
                                    n_random_lines))
        
        # write index header
        fout_index.write("doc1_id,doc2_id\n")

        # create the new dataset with id2 as
        # the line number in the file

        line_index = 1
        
        for line in fin:
            # match = re.search(r"\{.*?\}", line)

            original_line_dict = json.loads(line.strip())

            if write_original_lines:
                original_line_dict[id_int_link_field_name] = "None" # id3
                
                json.dump(original_line_dict, fout)  # use json.dump here
                fout.write("\n")  # add a newline after each json object

            if line_index in edit_indexes:
                
                edited = EditDict(dictionary = original_line_dict,
                                  id_int_unique_last_index = id_int_unique_last_index, # id2 last value
                                  id_int_unique_field_name = id_int_unique_field_name, # id2
                                  id_int_link_field_name = id_int_link_field_name, # id3
                                  content_field_name = content_field_name,
                                  functions_params_list = functions_params_list,
                                  functions_edit_list = functions_edit_list)

                json.dump(edited, fout)  # use json.dump here
                fout.write("\n")  # add a newline after each json object

                # write the pair (original_doc_id, duplicated_doc_id) in the index file
                # first column: original file id
                # second column: duplicate file id
                id_int_unique_last_index += 1
                fout_index.write(f"{original_line_dict[id_int_unique_field_name]},{id_int_unique_last_index}\n")
                    
                
                
            line_index += 1

# idea: write it as a dictionary, save as a json
# and reload as dictionary as needed
def WriteMetadataCollection(param_names_list: list,
                            param_values_list: list,
                            file_out_path: str):
    '''Write metadata with collection parameters:
    '''
    temp_dict = {"collection_params": dict(zip(param_names_list, param_values_list))}
    with open(file_out_path, "w") as fout:
        json.dump(temp_dict, fout)