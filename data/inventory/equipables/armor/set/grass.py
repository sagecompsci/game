from templates.armor_template import write_file_armor_same


title = "Grass"
key = "grass"
types = [
    "_headband",
    "_sash",
    "_skirt",
    "_sandals"
]
properties = {
    "head_name": f"{title} Headband",
    "chest_name": f"{title} Sash",
    "legs_name": f"{title} Skirt",
    "feet_name": f"{title} Sandals",

    "head_description": "A simple headband made from woven grass.",
    "chest_description": "A simple sash made from woven grass",
    "legs_description": "A simple skirt made from woven grass.",
    "feet_description": "Simple sandals made from woven grass. They aren't very comfortable, but they're better than nothing",

    "effects": {"health": 1},
    "bonus": 1,
    "requirements": {},
    "locations": [],
}

write_file_armor_same(types, key, properties)
