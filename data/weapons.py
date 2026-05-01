from collections import namedtuple
Weapon = namedtuple("Weapon", ["name", "description", "type", "effects", "requirements", "locations"])

weapon_data = {
    "wood_club": Weapon (
        name = "Wood Club",
        description = "A simple wood club.",
        type = "weapons",
        effects = {"strength": 1},
        requirements = {},
        locations = [],
    ),
    "wood_mace": Weapon (
        name = "Wood Mace",
        description = "A mace carved from wood. Those wooden spikes look like they could do some damage.",
        type = "weapons",
        effects = {"strength": 2},
        requirements = {},
        locations = [],
    ),
    "spiked_wood_club": Weapon (
        name = "Spiked Wood Club",
        description = "Metal spikes have been affixed to a wood club. It's heavy.",
        type = "weapons",
        effects = {"strength": 3},
        requirements = {"strength": 5},
        locations = [],
    ),

    "sword": Weapon (
        name = "Sword",
        description = "This is a sword that does swordy things",
        type = "weapons",
        effects = {"strength": 5},
        requirements = {},
        locations = "maze chest",
    ),

    "dagger": Weapon(
        name = "Dagger",
        description = "This is a very stabby dagger",
        type = "weapons",
        effects = {"attack_speed": 3, "strength": 2},
        requirements = {},
        locations = "maze chest",
    )
}