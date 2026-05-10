import pyray as rl

from classes.my_dataclasses import GameState
import save
import create_menus
from generate_levels.generate_one import create_level as create_one

def get_save_name(name: str):
    key = rl.get_char_pressed()

    while key > 0:
        if (48 <= key <= 57) or (65 <= key <= 90) or (97 <= key <= 122) or key == 32:
            # numbers            #uppercase           #lowercase           #space
            name += chr(key)

        key = rl.get_char_pressed()

    if rl.is_key_pressed(rl.KeyboardKey.KEY_BACKSPACE):
        name = name[:-1]

    return name


def menu(state: GameState, main_title, main_buttons, load_buttons, new_input, pause_buttons):
    while rl.window_should_close() == False and state.view != "":
        mouse_pos = rl.Vector2(-1000, -1000)
        if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            mouse_pos = rl.get_mouse_position()

        if state.view == "main":
            state.save = ""
            for b in main_buttons:
                if b.pos.x <= mouse_pos.x <= b.pos.x + b.width and b.pos.y <= mouse_pos.y <= b.pos.y + b.height:
                    state.view = b.on_click()

        elif state.view == "load":
            if rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
                state.view = "main"
            for b in load_buttons:
                if b.pos.x <= mouse_pos.x <= b.pos.x + b.width and b.pos.y <= mouse_pos.y <= b.pos.y + b.height:
                    state.view = ""
                    state.save = b.text
                    save.load(b.text, state)

        elif state.view == "new":
            if rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
                state.view = "main"
            state.save = get_save_name(state.save)
            new_input.text = state.save
            if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER):
                if state.save != "":
                    state.view = ""

                one = state.levels["one"]
                start_pos, one["tiles"], one["monsters"], one["chests"], state.buildings["one"] = create_one(state.tile_size, state.map_size)
                state.player.pos = rl.Vector2(start_pos.x, start_pos.y)
                state.camera.target = rl.Vector2(state.player.pos.x, state.player.pos.y)
                state.map = state.levels[state.level]

        elif state.view == "pause":
            for b in pause_buttons:
                if b.pos.x <= mouse_pos.x <= b.pos.x + b.width and b.pos.y <= mouse_pos.y <= b.pos.y + b.height:
                    state.view = b.on_click()
                    save.save(state)

            if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER):
                state.view = ""

        rl.begin_drawing()
        rl.clear_background(rl.WHITE)

        if state.view == "main":
            create_menus.draw_main_menu(state.textures, main_title, main_buttons)
        elif state.view == "load":
            create_menus.draw_load_menu(state.textures, load_buttons, state.font)
        elif state.view == "new":
            create_menus.draw_new_menu(state.font, state.textures, new_input)
        elif state.view == "pause":
            create_menus.draw_pause_menu(state.textures, pause_buttons)

        rl.end_drawing()
