import json

def ToJsonLineRead(my_match: str,
                   id_name: str,
                   content_name: str) -> tuple:
    '''
    Given a match (i.e a string which matches with some criteria, output of other function)
    of a json, with a id and content field names, return the id and content values in a tuple.
    
    Args:
        - my_match (str): string, assuming it satisifies some already checked criteria
        - id_name (str): name of the id field
        - content_name (str): name of the content field
    Return:
        - tuple (tuple): (id_value, content_value)
    
    '''
    content = my_match.group(0)  # group(0) returns the entire match
    # due to json problems
    json_content = json.loads(content)  # Convert the content to JSON
    id_temp = int(json_content[id_name])
    text_temp = json_content[content_name]
    
    return (id_temp, text_temp)

