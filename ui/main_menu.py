import pyray as rl
from utilities import utilities as u
from information import views
from information.ui import (
    scale,
    font_size,
    spacing,
    color,
    text_box_small_size as box_size,
    text_box_small_padding as box_padding
)



def main_menu(textures: dict[str, rl.Texture], font: rl.Font) -> str:
    """

    :param textures: dictionary of textures
    :param font: default font
    :return: state.view
    """

    screen_width = rl.get_screen_width()
    screen_height = rl.get_screen_height()

    title_size = rl.Vector2(61 * scale, 27 * scale)

    t_width = 192
    t_height = 108
    title_screen_size = rl.Vector2(192 * scale, 108 * scale)
    t_scale = scale


    while screen_width > t_width * t_scale or screen_height > t_height * t_scale:
        t_scale += 1


    title_margin = title_size.x//10
    title_pos = rl.Vector2(title_margin, screen_height//2 - title_size.y)
    title_center = title_pos.x + title_size.x//2

    box_pos = rl.Vector2(title_center - box_size.x//2, title_pos.y + title_size.y + title_margin)


    view = views.main_menu
    mouse = rl.get_mouse_position()

    rl.draw_texture_ex(textures["title_screen"], rl.Vector2(0, 0), 0, t_scale, rl.WHITE)
    rl.draw_texture_ex(textures["title"], title_pos, 0, scale, rl.WHITE)


    options = [views.new_menu, views.load_menu]

    pos = rl.Vector2(box_pos.x, box_pos.y)
    for option in options:
        rl.draw_texture_ex(textures["text_box_small"], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)
        rl.draw_text_ex(font, option, rl.Vector2(pos.x + box_padding.x, pos.y + box_padding.y), font_size, spacing, color)

        if u.mouse_hovering(pos, mouse, box_size):
            rl.draw_texture_ex(textures["text_box_small_highlight"], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)
            if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
                view = option



        pos.y += box_size.y + scale

    return view
