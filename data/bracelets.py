from collections import namedtuple
Bracelet = namedtuple("Bracelet", ["name", "description", "type", "effects", "requirements", "locations"])

item_type = "bracelets"
bracelet_data = {
    "grass_cuff": Bracelet (
        name = "Grass Cuff",
        description = "A simple cuff made from woven grass. It's very itchy.",
        type = item_type,
        effects = {"health": 2},
        requirements = {},
        locations = ["crafting"]
    ),
    "simple_bracelet": Bracelet(
        name = "Simple Bracelet",
        description = "It's not very pretty",
        type = item_type,
        effects = {"strength": 2},
        requirements = {},
        locations = ["drops monster"],
    ),
    "sturdy_bracelet": Bracelet(
        name = "Sturdy Bracelet",
        description = "It's heavy",
        type = item_type,
        effects = {"defense": 5},
        requirements = {"strength": 5},
        locations = ["drops monster"],
    ),
}