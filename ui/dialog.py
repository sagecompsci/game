import pyray as rl
from classes.Npc import Npc
from classes.Enum import Status
from classes.DialogInfo import DialogInfo
from classes.Quest import KillQuest, Quest
from information import views
from utilities import utilities as u

from information.ui import (scale, font_size, text_font_size, spacing, color,
                            text_box_large_size, text_box_large_padding, text_box_small_size, text_box_small_padding,
                            )

center = rl.Vector2(rl.get_screen_width()//2, rl.get_screen_height()//2)
text_box_pos = rl.Vector2(center.x - text_box_large_size.x//2, center.y - text_box_large_size.y//2)
text_start = rl.Vector2(text_box_pos.x + text_box_large_padding.x, text_box_pos.y + text_box_large_padding.y)
text_end = rl.Vector2(text_box_pos.x + text_box_large_size.x - text_box_large_padding.x, text_box_pos.y + text_box_large_size.y - text_box_large_padding.y)

name_box_pos = rl.Vector2(text_box_pos.x, text_box_pos.y - scale - text_box_small_size.y)
name_pos = rl.Vector2(name_box_pos.x + text_box_small_padding.x, name_box_pos.y + text_box_small_padding.y)

options_pos = rl.Vector2(text_box_pos.x + text_box_large_size.x + 3 * scale, text_box_pos.y)
# if hovering over text box it moves -2x and gets highlight around the edge

def get_variables(text: str) -> list[str]:
    indexes = []
    for i in range(len(text)):
        if text[i] in ("{", "}"):
            indexes.append(i)
        elif i == 0:
            indexes.append(0)
        elif i == len(text) - 1:
            indexes.append(len(text))

    words = []
    for i in range(len(indexes)):
        if i != len(indexes) - 1:
            end = indexes[i + 1]
            start = indexes[i]
            if text[indexes[i]] == "}":
                start += 1

            words.append(text[start:end])

    return words

def get_new_text(text: str, quest: Quest) -> str:
    words = get_variables(text)
    new_text = ""
    for word in words:
        if word[0] == "{":
            variable = word[1: len(word)]
            word = quest.__getattribute__(variable)
        new_text += str(word)

    return new_text


def get_next_dialog(next_code: int, quest_status: Status, is_complete: bool, dialog_info: DialogInfo):
    new_code = next_code
    end = False
    if next_code == 0:
        end = True
        if quest_status == Status.available:
            new_code = dialog_info.quest_none
        elif quest_status == Status.active:
            new_code = dialog_info.quest_accepted
        elif quest_status == Status.complete:
            new_code = dialog_info.quest_rewarded

    else:
        if quest_status == Status.available and next_code == dialog_info.accept_dialog:
            quest_status = Status.active
        elif quest_status == Status.active and next_code == dialog_info.give_reward:
            if is_complete:
                quest_status = Status.need_reward
                new_code = dialog_info.quest_rewarded
            else:
                new_code = dialog_info.quest_not_complete

    return new_code, quest_status, end

def draw_text_box(textures, font: rl.Font, name: str, dialog_text: str):
    # Draw text box and dialog
    rl.draw_texture_ex(textures["text_box_large"], text_box_pos, 0, scale, rl.WHITE)
    u.draw_text(font, dialog_text, text_start, font_size, spacing, color, text_end.x - text_start.x)
    # lines = u.wrap_lines(font, dialog_text, font_size, spacing, int(text_end.x - text_start.x))
    # u.draw_wrapped_text(font, lines, text_start, font_size, spacing, color)

    # Draw name box and name
    rl.draw_texture_ex(textures["text_box_small"], name_box_pos, 0, scale, rl.WHITE)
    rl.draw_text_ex(font, name, name_pos, font_size, spacing, color)

def draw_options(textures, font: rl.Font, options: dict, dialog_code: int) -> int:
    pos = rl.Vector2(options_pos.x, options_pos.y)
    mouse = rl.get_mouse_position()

    for text, code in options.items():
        x = 0
        if pos.x < mouse.x < pos.x + text_box_small_size.x and pos.y < mouse.y < pos.y + text_box_small_size.y:
            x -= 2 * scale
            # If you click on an option
            if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
                return code
                # dialog_code, quest_status, end = get_next_dialog(code, quest_status, all_dialog)
                #
                # if end:
                #     menu = ""

        rl.draw_texture_ex(textures["text_box_small"], rl.Vector2(pos.x + x, pos.y), 0, scale, rl.WHITE)
        rl.draw_text_ex(font, text, rl.Vector2(pos.x + x + text_box_small_padding.x, pos.y + text_box_small_padding.y), text_font_size, spacing, color)


        if x == -2 * scale:
            rl.draw_texture_ex(textures["text_box_small_highlight"], rl.Vector2(pos.x + x, pos.y), 0, scale, rl.WHITE)

        pos.y += scale + text_box_small_size.y

    return dialog_code


def draw_dialog(view: str, textures, font: rl.Font, npc: Npc, quest: Quest):
    dialog = npc.dialogs[npc.dialog_code]

    # Draw text box and npc name
    text = dialog.text
    if "{" in text:
        text = get_new_text(text, quest)
    draw_text_box(textures, font, npc.name, text)


    npc.dialog_code = draw_options(textures, font, dialog.options, npc.dialog_code)
    npc.dialog_code, quest.status, end = get_next_dialog(npc.dialog_code, quest.status, quest.is_complete, npc.dialog_info)

    if end:
        view = views.game

    return view

