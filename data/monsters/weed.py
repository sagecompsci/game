from collections import namedtuple

Monster = namedtuple("Monster", ["name", "description", "health", "defense", "strength", "attack_speed", "speed",
                                 "stats", "drops", "locations"] )

name = "Weed"
weak_name = f"Weak {name}"
strong_name = f"Strong {name}"

description = "Many blades of grass have formed a \"mighty\" colony. They give you paper cuts, which will be very irritating for many days.",
weak_description = "A few blades of grass that have teamed up. Their attacks tickle more than they hurt."
strong_description = "Dozens of colonies have come together under the rule of their glorious and beautiful leader, Dandelion."

# weed? Their stubborn roots reach far into the ground

health = 2
weak_health = health/2
strong_health = health * 2

defense = 0
weak_defense = defense
strong_defense = 1

strength = 2
weak_strength = strength /2
strong_strength = strength * 3

attack_speed = 1
weak_attack_speed = attack_speed
strong_attack_speed = attack_speed * 2

speed = 0
weak_speed = 0
strong_speed = 0

stats = {"health": 1}
weak_stats = {"health": 1}
strong_stats = {"health": 2}

drops = {"grass": 1}
weak_drops = {}
strong_drops = {"grass": 2, "dandelion": 1}

locations = ["Everywhere under the open sky"]
weak_locations = locations.copy()
strong_locations = locations.copy()


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
