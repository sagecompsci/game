import pyray as rl
from importlib import reload

from save import save_game
from initialize.init import init
from game_loop import game_loop
from utilities.inventory_util import edit_inventory
from ui.menu_loop import menu
from information import views
from ui import inventory_ui as inventory, dialog


def main():
    state = init()

    reload(inventory)
    reload(dialog)

    inv_test(state)

    while not rl.window_should_close():
        if rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
            pass

        if state.view in views.menu_loop:
            state = menu(state.textures, state.font, state.view, state)

        elif state.view in views.gameplay_loop:
            game_loop(state)

        else:
            raise ValueError("state.view has not been assigned a proper value")

    if state.save != "":
        save_game(state.save, state.to_dict())

def inv_test(state):
    i = state.inventory
    edit_inventory(i, "grass_headband", 10)
    edit_inventory(i, "grass_sash", 10)
    edit_inventory(i, "grass_skirt", 10)
    edit_inventory(i, "grass_sandals", 10)

    edit_inventory(i, "grass_cuff", 10)
    edit_inventory(i, "ancient_ring", 10)

    edit_inventory(i, "apple", 10)
    edit_inventory(i, "grass", 10)
    edit_inventory(i, "leaf", 10)
    edit_inventory(i, "wood", 10)
    edit_inventory(i, "mushroom", 10)
    edit_inventory(i, "raw_drumstick", 10)

    edit_inventory(i, "cooked_drumstick", 10)

    edit_inventory(i, "journal", 10)

main()
