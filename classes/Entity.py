from dataclasses import dataclass

@dataclass
class Entity:
    """
    name: str - Capital Name of entity

    image: str - snake_case key to textures[image] for rl.Texture

    health: int - current health of entity

    max_health: int - max health of entity

    defense: int - defense of entity

    strength: int - strength of entity

    attack_speed: int - attack speed of entity

    speed: int - walking speed of entity

    last_attack: int - time of last time entity attacked

    stats: dict[str, int] - stats that the entity drops on death

    drops: dict[str, int] - items that entity drops on death

    locations: list[str] - locations that entity can be found
    """
    name: str
    image: str
    health: float
    max_health: float
    defense: float
    strength: float
    attack_speed: float
    speed: float
    last_attack: int
    stats: dict[str, int]
    drops: dict[str, int]
    locations: list[str]
