from collections import namedtuple
Ring = namedtuple("Ring", ["name", "description", "type", "effects", "requirements", "locations"])

item_type = "rings"

ring_data = {
    "dandelion_ring": Ring(
        name = "Dandelion Ring",
        description = "A beautiful ring made with grass and a dandelion.",
        type = item_type,
        effects = {"strength": 1},
        requirements = {"health": 5},
        locations = ["crafting"]
    ),
    "ring_one": Ring(
        name = "Ring Two",
        description = "This is the first ring.",
        type = item_type,
        effects = {"strength": 1},
        requirements = {},
        locations = ["drops monster"],
    ),
    "ring_two": Ring(
        name = "Ring Two",
        description = "This is the second ring.",
        type = item_type,
        effects = {"attack_speed": 1},
        requirements = {},
        locations = ["drops monster"],
    ),
    "ring_three": Ring(
        name = "Ring Three",
        description = "This ring has a requirement.",
        type = item_type,
        effects = {"defense": 1},
        requirements = {"attack_speed": 10},
        locations = ["drops monster"]
    )
}