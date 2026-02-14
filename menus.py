import pyray as rl
import os

import utilities as u
from my_dataclasses import Button

def x_center_screen(width: int) -> int:
    center = rl.get_screen_width()//2
    return center - (width//2)

def y_center_screen(height: int) -> int:
    center = rl.get_screen_height()//2
    return center - (height//2)

scale = 2


def create_main_menu() -> tuple[tuple[rl.Vector2, str], list[Button]]:
    title_width = 64
    title_pos = rl.Vector2(x_center_screen(title_width), rl.get_screen_height()//2)
    title_type = "title"
    title_height = 32

    title_margin = 20
    button_margin = 10

    new = Button (
        pos = rl.Vector2(0, 0),
        width = 64*scale,
        height = 32*scale,
        scale = scale,
        text = "",
        text_pos = rl.Vector2(0, 0),
        type = "new",
        on_click = lambda: "new",
    )
    load = Button (
        pos = rl.Vector2(0, 0),
        width = 64*scale,
        height = 32*scale,
        scale = scale,
        text = "",
        text_pos = rl.Vector2(0, 0),
        type = "load",
        on_click = lambda: "load",
    )


    new.pos = rl.Vector2(x_center_screen(new.width), title_pos.y + title_height + title_margin)
    load.pos = rl.Vector2(x_center_screen(load.width), new.pos.y + new.height + button_margin)
    buttons = [new, load]


    title = (title_pos, title_type)
    return title, buttons

def draw_main_menu(textures, title: tuple[rl.Vector2, str], buttons: list[Button]):
    rl.draw_texture_ex(textures[title[1]], title[0], 0, 1, rl.WHITE)

    for button in buttons:
        rl.draw_texture_ex(textures[button.type], button.pos, 0, button.scale, rl.WHITE)

def create_load_menu() -> list:
    buttons = []

    width = 64 * scale
    height = 16 * scale
    pos = rl.Vector2(x_center_screen(width), rl.get_screen_height()//2)

    files = os.listdir("saves")
    for file in files:
        save_name = file.split(".")[0]
        button = Button (
            pos = rl.Vector2(pos.x, pos.y),
            width = width,
            height = height,
            scale = scale,
            text = save_name,
            text_pos = rl.Vector2(pos.x + (10 * scale), pos.y + (5 * scale)),
            type = "save_file",
            on_click = lambda: "load",
        )
        buttons.append(button)
        pos.y += height + (20 * scale)

    return buttons

def draw_load_menu(textures, buttons: list):
     for button in buttons:
         rl.draw_texture_ex(textures[button.type], button.pos, 0, button.scale, rl.WHITE)
         rl.draw_text(button.text, int(button.text_pos.x), int(button.text_pos.y), 9 * scale, rl.BLACK)


def create_new_menu() -> Button:
    width = 64 * scale
    height = 16 * scale

    pos = rl.Vector2(x_center_screen(width), rl.get_screen_height() // 2)

    button = Button (
        pos = rl.Vector2(pos.x, pos.y),
        width = width,
        height = height,
        scale = scale,
        text = "",
        text_pos = rl.Vector2(pos.x + (10 * scale), pos.y + (5 * scale)),
        type = "save_file",
        on_click = lambda: "new",
    )


    return button

def draw_new_menu(textures, button: Button):
    rl.draw_texture_ex(textures[button.type], button.pos, 0, button.scale, rl.WHITE)
    rl.draw_text(button.text, int(button.text_pos.x), int(button.text_pos.y), 9 * scale, rl.BLACK)


def create_pause_menu() -> list[Button]:
    width =  64 * scale
    height = 16 * scale
    pos = rl.Vector2(x_center_screen(width), rl.get_screen_height()//2)
    resume = Button (
        pos = rl.Vector2(pos.x, pos.y),
        width = width,
        height = height,
        scale = scale,
        text = "Resume",
        text_pos = rl.Vector2(pos.x + (10 * scale), pos.y + (5 * scale)),
        type = "blank_button",
        on_click = lambda: "",
    )

    pos.y += height + 10
    main = Button(
        pos = rl.Vector2(pos.x, pos.y),
        width = width,
        height = height,
        scale = scale,
        text = "Main Menu",
        text_pos = rl.Vector2(pos.x + (10 * scale), pos.y + (5 * scale)),
        type = "blank_button",
        on_click=lambda: "main",
    )

    return [resume, main]

def draw_pause_menu(textures, buttons: list[Button]):
    for button in buttons:
        rl.draw_texture_ex(textures[button.type], button.pos, 0, button.scale, rl.WHITE)
        rl.draw_text(button.text, int(button.text_pos.x), int(button.text_pos.y), 9 * scale, rl.WHITE)

