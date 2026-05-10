import pyray as rl
from dataclasses import dataclass
from classes.Building import Building
from classes.Tile import Tile
from classes.Entity import Entity
from classes.Player import Player
from classes.Quest import Quest

@dataclass
class GameState:
    """
    save: str - save file

    player : Player - player information

    inventory: dict[str, dict[str, InventoryItem]] - list of inventory types
        - equips
        - weapons
        - armor
        - accessories
        - items
        - consumables
        - special

    gold: int - amount of the gold the player has

    quests: dict[str, set[int]] - "available", "active", "completed", keys for all_quests data

    kills: dict[str, int] - dictionary of kill count for each monster

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

    npc: str - str pos of current npc talking to

    inv_view: str - which inventory tab to display

    font: rl.Font - global font

    font_size: float - default font size
    """
    save: str
    player: Player
    inventory: dict[str, dict[str, int]]
    gold: int
    quests: dict[int, Quest]
    journal: dict
    level: str
    location: str
    map: dict
    levels: dict[str, dict[str, Tile | Building | Entity | tuple]]
    buildings: dict[str, dict[str, Tile | Building | Entity | tuple]]
    tile_size: int
    scale: int
    map_size: int
    textures: dict[str, rl.Texture]
    camera: rl.Camera2D
    time: int
    last_movement: int
    view: str
    npc: str
    inventory_view: str
    journal_view: str
    font: rl.Font
    font_size: float

    def to_dict(self) -> dict:
        return {
            "save": self.save,
            "player": self.player.to_dict(),
            "inventory": self.inventory,
            "gold": self.gold,
            "quests": self.quests,
            "journal": self.journal,
            "level": self.level,
            "location": self.location,
            "map": self.map,
            "levels": self.levels,
            "buildings": self.buildings,
            "time": self.time,
            "inventory_view": self.inventory_view,
            "journal_view": self.journal_view,
        }

    def from_dict(self, values) -> None:
        self.save = values["save"]
        self.player.from_dict(values["player"])
        self.inventory = values["inventory"]
        self.gold = values["gold"]
        self.quests = values["quests"]
        self.journal = values["journal"]
        self.level = values["level"]
        self.location = values["location"]
        self.map = values["map"]
        self.levels = values["levels"]
        self.buildings = values["buildings"]
        self.time = values["time"]
        self.last_movement = self.time
        self.inventory_view = values["inventory_view"]
        self.journal_view = values["journal_view"]
        # self.camera.target = rl.Vector2(self.player.pos.x, self.player.pos.y)



