from collections import namedtuple

Item = namedtuple("Item", ["name", "description", "type", "locations", "uses"])

items = "items"
special = "special"
consumables = "consumables"

item_data = {
    "grass": Item(
        name = "Grass",
        description = "A bundle of grass. This grass is tougher than normal. Maybe you could make something with it.",
        type = items,
        locations = ["drops,grass_tuft"],
        uses = ["craft armor"],

    ),
    "dandelion": Item (
        name = "Dandelion",
        description = "A beautiful dandelion",
        type = items,
        locations = ["drops,grass_tuft_strong"],
        uses = ["craft ring"],
    ),
    "leaf": Item (
        name = "Leaf",
        description = "A small leaf that was growing on a stump",
        type = items,
        locations = ["drops, stumpling"],
        uses = ["craft"]
    ),
    "mushroom": Item (
        name = "Mushroom",
        description = "A brightly colored mushroom, I wonder if it's poisonous...",
        type = items,
        locations = ["drops, stumpling_strong"],
        uses = ["craft"]
    ),
    "wood": Item (
        name = "Wood",
        description = "A solid chunk of wood. This will come in handy.",
        type = items,
        locations = ["drops, stumpling_weak"],
        uses = ["craft"]
    ),

    "journal": Item (
        name = "Journal",
        description = "A brand new journal to record your adventures in.",
        type = special,
        locations = ["npc"],
        uses = [],
    ),
    "map": Item (
        name = "Map",
        description = "A simple map that doesn't go into much detail.",
        type = special,
        locations = ["npc"],
        uses = []
    ),

    "apple": Item (
        name = "Apple",
        description = "A red fruit that tastes sweet.",
        type = consumables,
        locations = ["npc"],
        uses = []
    ),

}