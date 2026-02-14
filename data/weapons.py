from collections import namedtuple
Weapon = namedtuple("Weapon", ["name", "description", "type", "effects", "requirements", "locations"])

weapon_data = {
    "sword": Weapon(
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