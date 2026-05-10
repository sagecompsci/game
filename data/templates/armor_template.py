from templates.main_template import write_file

key = ""
title = ""
types = [

]

properties_same = {
    "head_name": f"{title} ",
    "chest_name": f"{title} ",
    "legs_name": f"{title} ",
    "feet_name": f"{title} ",

    "head_description": "",
    "chest_description": "",
    "legs_description": "",
    "feet_description": "",

    "effects": {},
    "bonus": 0,
    "requirements": {},
    "locations": [],
}

properties = {
    "head_name": f"{title} ",
    "chest_name": f"{title} ",
    "legs_name": f"{title} ",
    "feet_name": f"{title} ",

    "head_description": "",
    "chest_description": "",
    "legs_description": "",
    "feet_description": "",

    "head_effects": {},
    "chest_effects": {},
    "legs_effects": {},
    "feet_effects": {},

    "head_bonus": 0,
    "chest_bonus": 0,
    "legs_bonus": 0,
    "feet_bonus": 0,

    "head_requirements": {},
    "chest_requirements": {},
    "legs_requirements": {},
    "feet_requirements": {},

    "head_locations": [],
    "chest_locations": [],
    "legs_locations": [],
    "feet_locations": [],
}


property_names = [
    "name",
    "description",
    "effects",
    "requirements",
    "locations"
]

def write_file_armor_same(types: list[str], key: str, properties: dict):
    armor_types = ["head_", "chest_", "legs_", "feet_"]
    armors = {}
    path = ""

    for i in range(len(armor_types)):
        a_type = armor_types[i]
        type = types[i]
        armor = key + type
        armors[armor] = {}
        for property in property_names:
            if a_type in ("name", "description"):
                property_key = a_type + property
            else:
                property_key = property
            armors[armor][property] = properties[property_key]

        if "head" in a_type:
            path = "../head"
        if "chest" in a_type:
            path = "../chest"
        if "legs" in a_type:
            path = "../legs"
        if "feet" in a_type:
            path = "../feet"

        if path != "":
            file = f"{path}/{armor}.json"
            write_file(file, armors[armor])
