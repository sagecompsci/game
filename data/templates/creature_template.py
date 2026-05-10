import json
from templates.main_template import write_file

property_names = [
    # Name of creature as it appears in text
    "name",
    "description",
    "health",
    "defense",
    "strength",
    "attack_speed",
    "speed",
    # how many tiles away they can attack from, 1 tile means creature must be right next to player
    "attack_range",
    # how far they can go from their original position
    "territory",
    # how many tiles away combat will initiate, once you are out of range, combat will stop
    "combat_range",
    "stats",
    "drops",
    "locations"
]

key = ""
name = ""

properties = {
    "name_weak": f"Weak {name}",
    "name": f"{name}",
    "name_strong": f"Strong {name}",

    "description_weak": "",
    "description": "",
    "description_strong": "",

    "health_weak": 0,
    "health": 0,
    "health_strong": 0,

    "defense_weak": 0,
    "defense": 0,
    "defense_strong": 0,

    "strength_weak": 0,
    "strength": 0,
    "strength_strong": 0,

    "attack_speed_weak": 0,
    "attack_speed": 0,
    "attack_speed_strong": 0,

    "speed_weak": 0,
    "speed": 0,
    "speed_strong": 0,

    "attack_range_weak": 0,
    "attack_range": 0,
    "attack_range_strong": 0,

    "territory_weak": 0,
    "territory": 0,
    "territory_strong": 0,

    "combat_range_weak": 0,
    "combat_range": 0,
    "combat_range_strong": 0,

    "stats_weak": {},
    "stats": {},
    "stats_strong": {},

    "drops_weak": {},
    "drops": {},
    "drops_strong": {},

    "locations_weak": [],
    "locations": [],
    "locations_strong": [],
}


def write_file_aggressive(key: str, properties: dict):
    creatures = {}

    for level in ["_weak", "", "_strong"]:
        creature = key + level
        creatures[creature] = {}
        for property in property_names:
            property_key = property + level
            creatures[creature][property] = properties[property_key]

        file = f"../{creature}.json"
        write_file(file, creatures[creature])