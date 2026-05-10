import os
import json
path = os.getcwd()


def update(path: str, inventory: str, type: str):
    for file in os.listdir(path):
        file_path = f"{path}/{file}"
        new_inventory = inventory
        new_type = type

        if os.path.isdir(file_path):
            if file in ["consumables", "accessories", "armor", "weapons", "items", "special"]:
                new_inventory = f"{file}"
            new_type = file

            if file != "set":
                update(file_path, new_inventory, new_type)

        elif file.split(".")[1] == "json":
            with open(file_path, "r") as f:
                item = json.load(f)
                item["type"] = new_type
                item["inventory"] = new_inventory
            with open(file_path, "w") as f:
                f.write(json.dumps(item, indent = 4))

update(path, "", "")

