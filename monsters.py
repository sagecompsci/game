from collections import namedtuple
Monster = namedtuple("Monster", ["name", "health", "max_health", "defense", "attack", "speed",
                                 "xp", "drops", "locations"] )

monster_data = {
    "minotaur": Monster(
        name="Minotaur",
        health=10,
        max_health=1,
        defense=0,
        attack=0,
        speed=1,
        xp=10,
        drops=["minotaur_horn"],
        locations=["maze"],
    ),

    "gargoyle": Monster(
        name="Gargoyle",
        health=10,
        max_health=1,
        defense=0,
        attack=0,
        speed=1,
        xp=20,
        drops=["living_stone"],
        locations=["maze"]
    )
}