from typing import Callable, Any
import pyray as rl
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
    bonus_health: int
    bonus_defense: int
    bonus_strength: int
    bonus_attack_speed: int
    bonus_speed: int


@dataclass
class InventoryItem:
    """
    count: int - amount of item

    type: str - type of weapons, corresponds to data file
    """
    count: int
    type: str

@dataclass
class Tile:
    """
    rotation: int - rotation of the tile

    tile: str - name of tile image

    directions: list[str] - list of directions the player can move once on the tile
    """
    rotation: int
    name: str
    directions: list[str]

@dataclass
class Building:
    """
    rotation: int - rotation of the building

    width: int - the width of the building in tiles

    height: int - the height of the building in tiles

    name: str - name of building image

    tiles: list[str] - all the tiles that the building occupies
    """
    rotation: int
    width: int
    height: int
    name: str

@dataclass
class Button:
    """
    pos: rl.Vector2 - position of the button

    width: int - width of the button

    height: int - height of the button

    scale: int - scale to draw button

    text: str - text on the button

    text_pos: rl.Vector2 - position of text

    type: str - name of image to draw

    on_click: Callable[..., Any] - function to call on click
    """
    pos: rl.Vector2
    width: int
    height: int
    scale: int
    text: str
    text_pos: rl.Vector2
    type: str
    on_click: Callable[..., Any]

@dataclass
class GameState:
    """
    save: str - save file

    player : Player - player information

    inventory: dict[str, dict[str, InventoryItem]] - list of inventory types
        - equips
        - weapons
        - armor
        - necklaces
        - bracelets
        - rings
        - items

    gold: int - amount of the gold the player has

    locations: str - current locations of player ex "map", "building", "cave"

    level: str - ex "one", "two", "three"

    locations: str - ex "levels", "buildings"

    view: dict - current map to draw

    levels: dict[str, dict[str, Tile]] - a dictionary of each dictionary for the tiles in a level


    buildings: dict[str, dict] - a dictionary of layouts of houses based on door position

    chests: dict[str, dict[str, str]] - a dictionary of each dictionary for the chests in a level

    monsters: dict[str, dict[str, Entity]] - a dictionary of each dictionary for the monsters in a level

    tile_size: int - width/height of each tile in pixels (will be multiplied by scale)

    scale: int - how much to multiple tile size by, also scale value for rl.draw_texture_ex

    map_size: int - width/height of map in tiles

    textures: dict[str, rl.Texture] - a dictionary of all textures for each image

    camera: rl.Camera2D - the camera that follows the player

    time: int - time since game start. 60 frames per second

    last_movement: int - time since player last moved

    menu: str - which menu to view

    inv_view: str - which inventory tab to display
    """
    save: str
    player: Player
    inventory: dict[str, dict[str, InventoryItem]]
    gold: int
    level: str
    location: str
    view: dict
    levels: dict[str, dict[str, Tile | Building | Entity | tuple]]
    buildings: dict[str, dict[str, Tile | Building | Entity | tuple]]
    tile_size: int
    scale: int
    map_size: int
    textures: dict[str, rl.Texture]
    camera: rl.Camera2D
    time: int
    last_movement: int
    menu: str
    inv_view: str

