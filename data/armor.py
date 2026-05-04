from collections import namedtuple
Armor = namedtuple("Armor", ["name", "description", "type", "effects", "requirements", "locations"])

armor = "armor"
head = "armor head"
chest = "armor chest"
legs = "armor legs"
feet = "armor feet"
armor_data = {
    "grass_headband": Armor(
        name = "Grass Headband",
        description = "A simple headband made from woven grass, adorned with a dandelion",
        type = head,
        effects = {"defense": 1},
        requirements = {},
        locations = ["craft"],
    ),
    "grass_sash": Armor(
        name = "Grass Sash",
        description = "A simple sash made from woven grass.",
        type = chest,
        effects = {"defense": 1},
        requirements = {},
        locations = ["craft"],
    ),
    "grass_skirt": Armor(
        name = "Grass Skirt",
        description = "A simple skirt made from woven grass.",
        type = legs,
        effects = {"defense": 1},
        requirements = {},
        locations = ["craft"],
    ),
    "grass_sandals": Armor(
        name = "Grass Sandals",
        description = "Simple sandals made from woven grass. They aren't very comfortable, but it's better than nothing.",
        type = feet,
        effects = {"defense": 1},
        requirements = {},
        locations = ["craft"],
    ),

}