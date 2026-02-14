from collections import namedtuple
Armor = namedtuple("Armor", ["name", "description", "type", "effects", "requirements", "locations"])

armor = "armor"
head = "armor head"
chest = "armor chest"
legs = "armor legs"
feet = "armor feet"
armor_data = {
    "grass_hat": Armor(
        name = "Grass Hat",
        description = "A hat that keeps the sun out of your eyes.",
        type = head,
        effects = {"defense": 1},
        requirements = {},
        locations = ["craft"],
    ),
    "grass_shirt": Armor(
        name = "Grass Shirt",
        description = "A simple shirt made from grass. It's very itchy.",
        type = chest,
        effects = {"defense": 1},
        requirements = {},
        locations = ["craft"],
    ),
    "grass_pants": Armor(
        name = "Grass Pants",
        description = "Simple pants made from grass. The bottoms are very frayed.",
        type = legs,
        effects = {"defense": 1},
        requirements = {},
        locations = ["craft"],
    ),
    "grass_shoes": Armor(
        name = "Grass Shoes",
        description = "They aren't very comfortable, but they're better than nothing.",
        type = feet,
        effects = {"defense": 1},
        requirements = {},
        locations = ["craft"],
    ),

}