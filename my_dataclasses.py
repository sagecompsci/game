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

    attack: int

    speed: int

    drops: list[str]

    locations: list[str]
    """
    name: str
    image: str
    health: int
    max_health: int
    defense: int
    attack: int
    speed: int
    drops: list[str]
    locations: list[str]

@dataclass
class Player:
    """
    pos: rl.Vector2

    image: str

    health: int

    level: int

    xp: int

    health: int

    max_health: int

    defense: int

    attack: int

    speed: int
    """
    pos: rl.Vector2
    image: str
    level: int
    xp: int
    health: int
    max_health: int
    defense: int
    attack: int
    speed: int


@dataclass
class InventoryItem:
    """
    count: int

    item: tuple
    """
    count: int
    item: tuple

@dataclass
class GameState:
    """
    save: str

    player : Player

    next_to: list

    inventory: dict

    gold: int

    maze: dict

    chests: dict

    monsters: dict

    tile_size: int

    maze_size: int

    textures: dict

    camera: rl.Camera2D

    time: int

    menu: str
    """
    save: str
    player: Player
    next_to: list
    inventory: dict
    gold: int
    maze: dict
    chests: dict
    monsters: dict
    tile_size: int
    maze_size: int
    textures: dict
    camera: rl.Camera2D
    time: int
    menu: str

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