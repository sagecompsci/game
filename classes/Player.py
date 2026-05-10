import pyray as rl
from dataclasses import dataclass

@dataclass
class Player:
    """
    pos: rl.Vector2 - position of player

    image: str - key to textures[image] of player

    health: int - current health of player

    max_health: int - max health of player

    defense: int - defense of player

    strength: int - strength of player

    attack_speed: int - attack speed of player

    speed: int - walk speed of player

    last_attack: int - time of last time player attacked

    bonus_health: int - extra max health gained through items

    bonus_defense: int - extra defense gained through items

    bonus_strength: int - extra strength gained through items

    bonus_attack_speed: int - bonus attack_speed gained through items

    bonus_speed: int - bonus walk speed gained through item
    """
    pos: rl.Vector2
    image: str
    health: int
    max_health: int
    defense: int
    strength: int
    attack_speed: int
    speed: int
    last_attack: int
    bonus_health: int = 0
    bonus_defense: int = 0
    bonus_strength: int = 0
    bonus_attack_speed: int = 0
    bonus_speed: int = 0

    def to_dict(self) -> dict:
        return {
            "pos_x": self.pos.x,
            "pos_y": self.pos.y,
            "image": self.image,
            "health": self.health,
            "max_health": self.max_health,
            "defense": self.defense,
            "strength": self.strength,
            "attack_speed": self.attack_speed,
            "speed": self.speed,
            "last_attack": self.last_attack,
        }

    def from_dict(self, values: dict) -> None:
        self.pos.x = values["pos_x"]
        self.pos.y = values["pos_y"]
        self.image = values["image"]
        self.health = values["health"]
        self.max_health = values["max_health"]
        self.defense = values["defense"]
        self.strength = values["strength"]
        self.attack_speed = values["attack_speed"]
        self.speed = values["speed"]
        self.last_attack = values["last_attack"]

