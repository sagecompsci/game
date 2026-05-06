import pyray as rl
import utilities as u
from npcs import Npc, Dialog
import quests
from quests import KillQuest

from ui_info import (scale, font_size, text_font_size, spacing, color,
                      text_box_large_size, text_box_large_margin, text_box_small_size, text_box_small_margin,
                     )

center = rl.Vector2(rl.get_screen_width()//2, rl.get_screen_height()//2)
text_box_pos = rl.Vector2(center.x - text_box_large_size.x//2, center.y - text_box_large_size.y//2)
text_start = rl.Vector2(text_box_pos.x + text_box_large_margin.x, text_box_pos.y + text_box_large_margin.y)
text_end = rl.Vector2(text_box_pos.x + text_box_large_size.x - text_box_large_margin.x, text_box_pos.y + text_box_large_size.y - text_box_large_margin.y)

name_box_pos = rl.Vector2(text_box_pos.x, text_box_pos.y - scale - text_box_small_size.y)
name_pos = rl.Vector2(name_box_pos.x + text_box_small_margin.x, name_box_pos.y + text_box_small_margin.y)

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

def get_new_text(text: str, quest: KillQuest) -> str:
    words = get_variables(text)
    new_text = ""
    for word in words:
        if word[0] == "{":
            variable = word[1: len(word)]
            word = quest.__getattribute__(variable)
        new_text += str(word)

    return new_text


def draw_text_box(textures, font: rl.Font, name: str, dialog: str):
    # Draw text box and dialog
    rl.draw_texture_ex(textures["text_box_large"], text_box_pos, 0, scale, rl.WHITE)
    lines = u.wrap_lines(font, dialog, font_size, spacing, int(text_end.x - text_start.x))
    u.draw_wrapped_text(font, lines, text_start, font_size, spacing, color)

    # Draw name box and name
    rl.draw_texture_ex(textures["text_box_small"], name_box_pos, 0, scale, rl.WHITE)
    rl.draw_text_ex(font, name, name_pos, font_size, spacing, color)

def draw_options(menu: str, textures, font: rl.Font, quest_status, quest_code: int, dialog: Dialog,
                 dialog_code: int, options: list[str], codes: list[int], quest_dialog: int, quest_option: int = None)\
                 -> tuple[int, str, str]:
    pos = rl.Vector2(options_pos.x, options_pos.y)
    mouse = rl.get_mouse_position()

    for key, option in dialog.options.items():
        x = 0
        if pos.x < mouse.x < pos.x + text_box_small_size.x and pos.y < mouse.y < pos.y + text_box_small_size.y:
            x -= 2 * scale
            # If you click on an option
            if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
                dialog_code, quest_status, end = dialog.on_click(key, quest_status)

                if end:
                    menu = ""



                # if type(quest_option) == int:
                #     # if you accepted a quest
                #     if answer_code == quest_option:
                #         quest_dialog = 0
                #         quests.give_quest(available_quests, active_quests, quest_code)
                #
                # # new dialog
                # dialog_code = codes[answer_code]
                #
                # # if conversation ends
                # if dialog_code == 0:
                #     menu = ""
                #
                #     # if quest has been accepted
                #     if quest_dialog == 0:
                #         # goes to default dialog
                #         dialog_code = codes[answer_code + 1]
                #
                #     else:
                #         # goes to quest dialog
                #         dialog_code = quest_dialog
                #

        rl.draw_texture_ex(textures["text_box_small"], rl.Vector2(pos.x + x, pos.y), 0, scale, rl.WHITE)
        rl.draw_text_ex(font, option, rl.Vector2(pos.x + x + text_box_small_margin.x, pos.y + text_box_small_margin.y), text_font_size, spacing, color)


        if x == -2 * scale:
            rl.draw_texture_ex(textures["text_box_small_highlight"], rl.Vector2(pos.x + x, pos.y), 0, scale, rl.WHITE)

        pos.y += scale + text_box_small_size.y

    return dialog_code, quest_status, menu


def draw_dialog(menu: str, textures, font: rl.Font, npc: Npc, all_quests: dict[int, KillQuest]):
    dialog = npc.dialogs[npc.dialog_code]
    quest = all_quests[npc.quest_code]

    # Draw text box and npc name
    text = dialog.text
    if npc.dialog_code in npc.variable_dialog:
        text = get_new_text(text, quest)
    draw_text_box(textures, font, npc.name, text)

    options = []
    codes = []

    npc.dialog_code, quest.status, menu = draw_options(menu, textures, font, quest.status,
                npc.quest_code, dialog, npc.dialog_code, options, codes, 1, 1)

    return menu

