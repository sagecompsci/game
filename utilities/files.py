import json

def read_file(path: str) -> dict:
    """
    returns a json object from a file as a dictionary
    :param path: string of the file path
    :return: dictionary of json object
    """
    with open(path, "r") as f:
        return json.load(f)

def write_file(path: str, content: dict) -> None:
    """
    writes a dictionary to a file as a json object
    :param path: string of the file path to write
    :param content: dictionary
    :return: None
    """
    with open(path, "w") as f:
        f.write(json.dumps(content, indent = 4))