from collections import namedtuple
Weapon = namedtuple("Weapon", ["name", "description", "type", "effects", "requirements", "locations"])

item_type = "weapons"

weapon_data = {
    "wood_sword": Weapon (
        name = "Wood Sword",
        description = "Despite being made from wood, it's still sharp enough to cut through monsters.",
        type = item_type,
        effects = {"strength": 1},
        requirements = {},
        locations = [],
    ),
    "wood_club": Weapon (
        name = "Wood Club",
        description = "A simple wood club.",
        type = item_type,
        effects = {"strength": 1},
        requirements = {},
        locations = [],
    ),
    "wood_mace": Weapon (
        name = "Wood Mace",
        description = "A mace carved from wood. Those wooden spikes look like they could do some damage.",
        type = item_type,
        effects = {"strength": 2},
        requirements = {},
        locations = [],
    ),
    "spiked_wood_club": Weapon (
        name = "Spiked Wood Club",
        description = "Metal spikes have been affixed to a wood club. It's heavy.",
        type = item_type,
        effects = {"strength": 3},
        requirements = {"strength": 5},
        locations = [],
    ),

    "sword": Weapon (
        name = "Sword",
        description = "This is a sword that does swordy things",
        type = item_type,
        effects = {"strength": 5},
        requirements = {},
        locations = "maze chest",
    ),

    "dagger": Weapon(
        name = "Dagger",
        description = "This is a very stabby dagger",
        type = item_type,
        effects = {"attack_speed": 3, "strength": 2},
        requirements = {},
        locations = "maze chest",
    )
}