from typing import Callable, Any
import pyray as rl
from dataclasses import dataclass

@dataclass
class Entity:
    """
    name: str

    image: str

    health: int

    max_health: int

    defense: int

    strength: int

    attack_speed: int

    speed: int

    last_attack: int

    stats: dict

    drops: dict

    locations: list[str]
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
    stats: dict
    drops: dict
    locations: list[str]

@dataclass
class Player:
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

    bonus_health: int

    bonus_defense: int

    bonus_strength: int

    bonus_attack_speed: int

    bonus_speed: int
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
    bonus_health: int
    bonus_defense: int
    bonus_strength: int
    bonus_attack_speed: int
    bonus_speed: int


@dataclass
class InventoryItem:
    """
    count: int

    type: str
    """
    count: int
    type: str

@dataclass
class GameState:
    """
    save: str

    player : Player

    next_to: list

    inventory: dict

    gold: int

    level: str

    maze: dict

    chests: dict

    maze_monsters: dict

    village_monsters: dict

    tile_size: int

    maze_size: int

    textures: dict

    camera: rl.Camera2D

    time: int

    menu: str

    inv_view: str
    """
    save: str
    player: Player
    next_to: list
    inventory: dict
    gold: int
    maze: dict
    chests: dict
    monsters: dict
    village_monsters: dict
    tile_size: int
    maze_size: int
    textures: dict
    camera: rl.Camera2D
    time: int
    menu: str
    inv_view: str

@dataclass
class Tile:
    """
    pos: rl.Vector2

    rotate_pos: rl.Vector2

    rotation: int

    tile: str

    directions: list[str]
    """
    pos: rl.Vector2
    rotate_pos: rl.Vector2
    rotation: int
    tile: str
    directions: list[str]

@dataclass
class Button:
    """
    pos: rl.Vector2

    width: int

    height: int

    scale: int

    text: str

    text_pos: rl.Vector2

    type: str

    on_click: Callable[..., Any]
    """
    pos: rl.Vector2
    width: int
    height: int
    scale: int
    text: str
    text_pos: rl.Vector2
    type: str
    on_click: Callable[..., Any]