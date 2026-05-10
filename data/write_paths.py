import os
import json
path = os.getcwd()


def create_dict(path: str, items: dict, data_path:str) -> dict:
    for file in os.listdir(path):
        file_path = f"{path}/{file}"
        new_data_path = f"{data_path}/{file}"

        if os.path.isdir(file_path):
            if file != "set":
                create_dict(file_path, items, new_data_path)
        else:
            name, extension = file.split(".")
            if extension == "json":
                items[name] = f"{new_data_path}"

    return items

def write_creatures(path: str):
    path = f"{path}/creatures"

    creatures = {}
    data_path = "data/creatures"
    creatures = create_dict(path, creatures, data_path)

    with open("creature_paths.json", "w") as f:
        f.write(json.dumps(creatures, indent = 4))

def write_inventory(path: str):
    path = f"{path}/inventory"

    inventory = {}
    data_path = "data/inventory"
    inventory = create_dict(path, inventory, data_path)
    with open("inventory_paths.json", "w") as f:
        f.write(json.dumps(inventory, indent = 4))

# write_creatures(path)
write_inventory(path)