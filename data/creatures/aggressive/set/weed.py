from templates.creature_template import write_file_aggressive

key = "weed"
name = "Weed"

# requirements - 8 health
properties = {
    "name_weak": f"Weak {name}",
    "name": f"{name}",
    "name_strong": f"Strong {name}",

    "description_weak": "Their stubborn roots reach far into the ground. Their attacks tickle more than they hurt.",
    "description": "Many blades of grass have formed a \"mighty\" colony. They give you paper cuts, which will be very irritating for many days.",
    "description_strong": "Dozens of colonies have come together under the rule of their glorious and beautiful leader, Dandelion.",

    "health_weak": 2,
    "health": 4,
    "health_strong": 2,

    "defense_weak": 0,
    "defense": 0,
    "defense_strong": 1,

    "strength_weak": 1,
    "strength": 2,
    "strength_strong": 2,

    "attack_speed_weak": 1,
    "attack_speed": 1,
    "attack_speed_strong": 1,

    "speed_weak": 0,
    "speed": 0,
    "speed_strong": 1,

    "attack_range_weak": 1,
    "attack_range": 1,
    "attack_range_strong": 2,

    "territory_weak": 0,
    "territory": 1,
    "territory_strong": 2,

    "combat_range_weak": 1,
    "combat_range": 1,
    "combat_range_strong": 1,

    "stats_weak": {"health": .25},
    "stats": {"health": .5},
    "stats_strong": {"health": 2},

    "drops_weak": {},
    "drops": {"grass": 1},
    "drops_strong": {"grass": 1, "dandelion": 1},

    "locations_weak": ["Everywhere under the open sky."],
    "locations": ["Only in the most neglected areas."],
    "locations_strong": [],
}


write_file_aggressive(key, properties)
