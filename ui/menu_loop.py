import pyray as rl
from information import views
from ui.main_menu import main_menu
from ui.new_menu import new_menu
from ui.load_menu import load_menu
from ui.pause_menu import pause_menu
from classes.GameState import GameState



def menu(textures: dict[str, rl.Texture], font: rl.Font, view: str, state: GameState) -> GameState:
    rl.begin_drawing()
    rl.clear_background(rl.WHITE)

    if view == views.main_menu:
        state.view = main_menu(textures, font)

    elif view == views.new_menu:
        state = new_menu(textures, font, state)

    elif view == views.load_menu:
        state = load_menu(textures, font, state)

    elif view == views.pause_menu:
        state.view = pause_menu(textures, font, state)

    rl.end_drawing()


    return state