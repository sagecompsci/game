import json
def write_file(file: str, properties: dict):
    with open(file, "w") as f:
        f.write(json.dumps(properties, indent = 2))

