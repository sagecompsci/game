from collections import namedtuple
Monster = namedtuple("Monster", ["name", "description", "health", "defense", "strength", "attack_speed", "speed",
                                 "stats", "drops", "locations"] )
Template = namedtuple("Template", ["name", "descriptions", "desc_index", "health", "defense",
            "strength", "attack_speed", "speed", "all_stats", "stats_key", "all_drops", "drops_key", "locations"])
"""
stumpling villages forest
grass tuft king drops is grass roots
"""

def create_monster(monster: Template) -> dict:
    monsters = {}
    levels = ["_weak", "", "_strong"]
    names = ["Weak ", "", "Strong "]
    for i in range(len(levels)):
        key = f"{monster.name}{levels[i]}"
        name = f"{names[i]}{monster.name}"
        new_name = name.replace("_", " ").title()
        j = i
        drops = {}
        while j > -1:
            if len(monster.drops_key) == 1:
                item = monster.drops_key[0]
            else:
                item = monster.drops_key[i]
            num = monster.all_drops[item]
            if item in drops.keys():
                drops[item] += num
            else:
                drops[item] = num
            j -= 1

        k = i
        stats = {}
        while k > -1:
            if len(monster.stats_key) == 1:
                stat = monster.stats_key[0]
            else:
                stat = monster.stats_key[k]
            num = monster.all_stats[stat]
            if stat in stats.keys():
                stats[stat] += num
            else:
                stats[stat] = num
            k -= 1

        if len(monster.desc_index) == 1:
            index = monster.desc_index[0]
        else:
            index = monster.desc_index[i]

        monsters[key] = Monster(
            name = new_name,
            description = monster.descriptions[index],
            health = monster.health[i],
            defense = monster.defense[i],
            strength = monster.strength[i],
            attack_speed = monster.attack_speed[i],
            speed = monster.speed[i],
            stats = stats,
            drops = drops,
            locations = monster.locations,
        )

    return monsters


def level_zero() -> dict:
    grass_stat_zero = [0, 1, 2]
    grass_stat_one = [1, 2, 3]
    grass_template = Template(
        name = "grass_tuft",
        descriptions = [
            "A few blades of grass that have teamed up. It looks as if it's attacking you, but it doesn't seem to be doing any damage.",
            "Many blades of grass have formed a \"mighty\" colony. They give you paper cuts, which will be very irritating for many days.",
            "Dozens of colonies have come together under the rule of their glorious and beautiful leader, Dandelion."
        ],
        desc_index = [0, 1, 1],
        health = grass_stat_one,
        defense = grass_stat_zero,
        strength = grass_stat_zero,
        attack_speed = grass_stat_one,
        speed = [0, 0, 0],
        all_stats = {"max_health": 1},
        stats_key = ["max_health"],
        all_drops = {"grass": 1},
        drops_key = ["grass"],
        locations = ["grasslands"]
    )

    monsters = {}
    monsters.update(create_monster(grass_template))

    return monsters





monster_data = {}
monster_data.update(level_zero())