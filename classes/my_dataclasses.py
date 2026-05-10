from typing import Callable, Any
import pyray as rl
from dataclasses import dataclass




@dataclass
class InventoryItem:
    """
    count: int - amount of item

    type: str - type of weapons, corresponds to data file
    """
    count: int
    type: str



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



