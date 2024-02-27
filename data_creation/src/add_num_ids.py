import sys
import json 
from typing import Callable

# convert all the ids to int and add a new id field
# to that field

def ConvertID(file_in: str,
              file_out: str,
              id_old_name: str,
              id_new_name: str,
              conv_fun: Callable) -> None:
    '''Write in file_out the lines of file_in with id_new added.
    
    Args: 
        - file_in:name of input file;
            each line of the file should be json like:
            {field1: "content",...}
        - file_out: output file name
        - id_old_name: name of the old id field name 
        - id_new_name: name of the old id field name
        - conv_fun: functions used to convert the id_old in the id_new
    
    Returns:
        - none
    '''
    with open(file_in, "r") as fin, open(file_out, "w") as fout:
        line_count = 0
        for line in fin:
            data = json.loads(line.strip())
            # get id
            id = data.get(id_old_name)
            new_id = conv_fun(id, line_count)
            
            data[id_new_name] = str(new_id)
            
            fout.write(json.dumps(data) + '\n')
            
            line_count += 1
            
            
            

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


def FromStrToIntOther(text: str, other: int) -> int:
    '''Convert Text to int.
    
    For all character in the string: convert all characters in int through
    the ord() function
    
    Args:
        - text: unused parameter, it'useful for other functions
        - other: return other
    Returns:
        - int: the converted int
    '''
    return other

# robust parameters:
# tipster_45_all_docs.json robust_2.json id id2 
# from command line:
# python .\near_duplicate_doc_lsh\data_creation\src\add_num_ids.py .\Data_Creation\tipster_45_all_docs.json robust_2.json id id2
def main():
    if len(sys.argv) < 5:
        print("No parameters given")
        return
    
    args = sys.argv[1:]
    ConvertID(args[0], args[1], args[2], args[3], FromStrToIntOther)


if __name__ == "__main__":
    main()