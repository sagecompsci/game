from collections import namedtuple
Necklace = namedtuple("Necklace", ["name", "description", "type", "effects", "requirements", "locations"])

necklace_data = {
    "simple_necklace": Necklace(
        name = "Simple Necklace",
        description = "A simple necklace that won't exist for long.",
        type = "necklaces",
        effects = {"health": 2},
        requirements = {},
        locations = ["drops monster"],
    ),
}
