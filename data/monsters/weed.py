from collections import namedtuple

Monster = namedtuple("Monster", [
    # printable name of monster
    "name",
    "description",
    "health",
    "defense",
    "strength",
    "attack_speed",
    "speed",
    "attack_range",
    "combat_range",
    "territory",
    "stats",
    "drops",
    "locations"
] )


name = "Weed"
weak_name = f"Weak {name}"
strong_name = f"Strong {name}"


weak_description = "Their stubborn roots reach far into the ground. Their attacks tickle more than they hurt."
description = "Many blades of grass have formed a \"mighty\" colony. They give you paper cuts, which will be very irritating for many days.",
strong_description = "Dozens of colonies have come together under the rule of their glorious and beautiful leader, Dandelion."

# weed? Their stubborn roots reach far into the ground

weak_health = 2
health = 4
strong_health = 2

weak_defense = 0
defense = 0
strong_defense = 1

weak_strength = 1
strength = 2
strong_strength = 2

weak_attack_speed = 1
attack_speed = 1
strong_attack_speed = 1

weak_speed = 0
speed = 0
strong_speed = 1

weak_attack_range = 1
attack_range = 1
strong_attack_range = 2

weak_territory = 0
territory = 1
strong_territory = 2

weak_stats = {"health": .25}
stats = {"health": .5}
strong_stats = {"health": 2}

weak_drops = {}
drops = {"grass": 1}
strong_drops = {"grass": 1, "dandelion": 1}

locations = ["Everywhere under the open sky"]
weak_locations = locations.copy()
strong_locations = locations.copy()

# requirements - 8 health

weed_weak = Monster (
    name = weak_name,
    description = weak_description,
    health = weak_health,
    defense = weak_defense,
    strength = weak_strength,
    attack_speed = weak_attack_speed,
    speed = weak_speed,
    stats = weak_stats,
    drops = weak_drops,
    locations = weak_locations
)

weed = Monster (
    name = name,
    description = description,
    health = health,
    defense = defense,
    strength = strength,
    attack_speed = attack_speed,
    speed = speed,
    stats = stats,
    drops = drops,
    locations = locations
)

weed_strong = Monster (
    name = strong_name,
    description = strong_description,
    health = strong_health,
    defense = strong_defense,
    strength = strong_strength,
    attack_speed = strong_attack_speed,
    speed = strong_speed,
    stats = strong_stats,
    drops = strong_drops,
    locations = strong_locations
)
