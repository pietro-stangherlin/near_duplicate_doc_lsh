import json
import random


def is_json(row):
    """
    Tests if a row is a valid JSON dictionary row.

    Examples:
        >>> row = {'id1': 2, 'id2': 'None', 'text': 'Pack my box with five dozen liquor jugs.'}
        >>> is_json(row)
        True
        >>> row = {'id1': 20}, # note the comma
        >>> is_json(row)
        False
        >>> row = [ # the usual start row of a json file
        >>> is_json(row)
        False

    Args:
        row (???): A row to elaborate.

    Returns:
        bool: If the passed row is a valid JSON dictionary row.
    """
    try:
        json_object = json.loads(row)
    except ValueError as e:
        return False
    return True


def read_n_random_json_elements(file_path, n = 10):
    """
    Selects n random rows from a JSON file. Returns only the real dictionary rows between those n selected rows.

    Examples:
        toy_data.json = 
        [
        {"id1": 1, "id2": "None", "text": "The quick brown fox jumps over the lazy dog."},
        {"id1": 2, "id2": "None", "text": "Pack my box with five dozen liquor jugs."},
        {"id1": 3, "id2": "None", "text": "Jackdaws love my big sphinx of quartz."},
        {"id1": 4, "id2": "None", "text": "How vexingly quick daft zebras jump!"},
        {"id1": 5, "id2": "None", "text": "Bright vixens jump; dozy fowl quack."},
        {"id1": 6, "id2": "None", "text": "Sphinx of black quartz, judge my vow."},
        {"id1": 7, "id2": "None", "text": "Quick zephyrs blow, vexing daft Jim."},
        {"id1": 8, "id2": "None", "text": "Two driven jocks help fax my big quiz."},
        {"id1": 9, "id2": "None", "text": "Five quacking zephyrs jolt my wax bed."},
        {"id1": 10, "id2": "None", "text": "Jinxed wizards pluck ivy from the big quilt."},
        {"id1": 11, "id2": "9", "text": "6ive quacking zephyrs joilt my wax bead."},
        {"id1": 12, "id2": "10", "text": "Jinx wiZards pLuck iwy from the big quit."}
        ]
        >>> read_n_random_json_elements("toy_data.json", n = 2)
        [{"id1": 2, "id2": "None", "text": "Pack my box with five dozen liquor jugs."},
        {"id1": 5, "id2": "None", "text": "Bright vixens jump; dozy fowl quack."}]
        >>> read_n_random_json_elements("toy_data.json", n = 2)
        [{"id1": 11, "id2": "9", "text": "6ive quacking zephyrs joilt my wax bead."}]
        # this appens if one of the n = 2 selected rows isn't a real dictionary 
        (in this case, there have been selected rows 1 (contains only "[") and 12 of toy_data.json)

    Args:
        file_path: The path of the JSON file to elaborate
        n (int): The desired number of rows to be selected

    Returns:
        dictionaries (list): A list containing the selected valid dictionary rows.
    """

    nLines = 0
    dictionaries = []
    
    with open(file_path, 'r') as file:
        
        # Counting number of lines of the JSON file
        for row in file:
            nLines += 1

        # Generating n random indexes, between 0 and nLines - 1
        indexes = random.sample(range(1, nLines), n)

        # Resetting the file pointer to the beginning of the file
        file.seek(0)

        # Populating dictionaries with selected elements (only real dictionaries)
        rowNumber = 0
        for row in file:
            rowNumber += 1
            row = row.strip() # prepares the row for the real dictionary test
            if row.endswith(","): # prepares the row for the real dictionary test
                row = row[:-1]
            if rowNumber in indexes and is_json(row):
                dictionaries.append(json.loads(row))
        
    return dictionaries


dics = read_n_random_json_elements("robust_2.json", 50)

len(dics)

# per scrivere su un nuovo file il nuovo json pulito
# (ovvero senza sporcizie dovute a randomNoise)
#with open("robust_tiny50_clean.json", 'w') as file:
 #   json.dump(dics, file, indent = 4)




