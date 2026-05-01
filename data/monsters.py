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
    levels = ["weak_", "", "strong_"]
    for i in range(len(levels)):
        key = f"{levels[i]}{monster.name}"
        new_name = key.replace("_", " ").title()
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

def level_one() -> dict:
    minotaur_template = Template(
        name = "minotaur",
        descriptions = ["A monster that has good smell"],
        desc_index = [0],
        health = [5, 5, 5],
        defense = [0, 0, 0],
        strength = [5, 5, 5],
        attack_speed = [1, 1, 1],
        speed = [1, 1, 1],
        all_stats = {"strength": 1},
        stats_key = ["strength"],
        all_drops = {"minotaur_horn": 1},
        drops_key = ["minotaur_horn"],
        locations = ["maze"],
    )

    gargoyle_template = Template(
        name = "gargoyle",
        descriptions = ["A stone monster"],
        desc_index = [0],
        health = [10, 10, 10],
        defense = [0, 0, 0],
        strength = [2, 2, 2],
        attack_speed = [2, 2, 2],
        speed = [1, 1, 1],
        all_stats = {"attack_speed": 1},
        stats_key = ["attack_speed"],
        all_drops = {"living_stone": 1},
        drops_key = ["living_stone"],
        locations = ["maze"],
    )

    monsters = {}
    monsters.update(create_monster(minotaur_template))
    monsters.update(create_monster(gargoyle_template))


    return monsters


monster_data = {}
monster_data.update(level_zero())
monster_data.update(level_one())