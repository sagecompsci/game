from dataclasses import dataclass

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
