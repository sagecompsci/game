from dataclasses import dataclass

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
