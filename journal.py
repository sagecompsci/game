import pyray as rl
from data.monsters import monster_data
from ui_info import scale, text_font_size, spacing, color

center = rl.Vector2(rl.get_screen_width()//2, rl.get_screen_height()//2)
offset = rl.Vector2(7 * scale, 2 * scale)
page_offset = 64 * scale

quest_offset = 2 * scale
pic_offset = 5 * scale

journal_size = rl.Vector2(121 * scale, 88 * scale)
picture_size = rl.Vector2(40 * scale, 24 * scale)
tab_size = rl.Vector2(9 * scale, 10 * scale)

journal_pos = rl.Vector2(center.x - journal_size.x//2, center.y - journal_size.y//2)
picture_pos = rl.Vector2(journal_pos.x + offset.x + pic_offset, journal_pos.y + offset.y + pic_offset)
picture_pos2 = rl.Vector2(journal_pos.x + page_offset + pic_offset, picture_pos.y)

quest_pos = rl.Vector2(journal_pos.x + offset.x + quest_offset, journal_pos.y + offset.y + quest_offset)
quest_pos2 = rl.Vector2(journal_pos.x + page_offset + quest_offset, quest_pos.y)

tab_pos = rl.Vector2(journal_pos.x + journal_size.x, journal_pos.y + 1 * scale)
tab_margin = 11 * scale


def draw_tabs(textures, tab_view: str):
    tabs = [
        "creatures",
        "quests",
        "equips",
        "recipes",
    ]
    pos = rl.Vector2(tab_pos.x, tab_pos.y)
    mouse = rl.get_mouse_position()

    for tab in tabs:
        x = 0
        if tab == tab_view:
            x -= 2 * scale
        rl.draw_texture_ex(textures[f"journal_tab_{tab}"], rl.Vector2(pos.x + x, pos.y), 0, scale, rl.WHITE)

        if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            if pos.x <= mouse.x <= pos.x + tab_size.x and pos.y <= mouse.y <= pos.y + tab_size.y:
                tab_view = tab

        pos.y += tab_margin


    return tab_view

def draw_creature(font: rl.Font, textures, creature: str, kills: dict):
    item = monster_data[creature]
    # Draw Picture
    rl.draw_texture_ex(textures[creature], rl.Vector2(picture_pos.x + scale, picture_pos.y + scale), 0, scale, rl.WHITE)
    rl.draw_texture_ex(textures["journal_picture"], rl.Vector2(picture_pos.x, picture_pos.y), 0, scale, rl.WHITE)

    # Draw Name
    pos = rl.Vector2(picture_pos.x, picture_pos.y + picture_size.y + pic_offset)
    rl.draw_text_ex(font, item.name, rl.Vector2(pos.x, pos.y), text_font_size, spacing, color)
    pos.y += quest_offset

    # Draw Count
    count = 0
    if creature in kills.keys():
        count = kills[creature]
    rl.draw_text_ex(font, f"{count} kills", rl.Vector2(pos.x, pos.y), text_font_size, spacing, color)

def draw_quests(font: rl.Font, active_quests: dict, completed_quests: dict):
    # draw active quests
    for quest in active_quests.values():
        monster_name = monster_data[quest.creature].name
        quest_name = f"{quest.type} {monster_name}"

        margin = 3 * scale
        pos = rl.Vector2(quest_pos.x, quest_pos.y)
        # Draw Name
        rl.draw_text_ex(font, quest_name, rl.Vector2(pos.x, pos.y), text_font_size, spacing, color)
        name_size = rl.measure_text_ex(font, quest_name, text_font_size, spacing)
        pos.x += name_size.x + margin

        # Draw kill count
        count = f"{quest.current_kills - quest.past_kills} / {quest.kill}"
        rl.draw_text_ex(font, count, rl.Vector2(pos.x, pos.y), text_font_size, spacing, color)
        monster_size =  rl.measure_text_ex(font, count, text_font_size, spacing)
        pos.x += monster_size.x + margin//2

        # Draw monster name
        rl.draw_text_ex(font, monster_name, rl.Vector2(pos.x, pos.y), text_font_size, spacing, color)

        pos.y += 10 * scale

    # Draw Completed Quests
    for quest in completed_quests.values():
        monster_name = monster_data[quest.creature].name
        quest_name = f"{quest.type} {monster_name}"

        margin = 10 * scale
        pos = rl.Vector2(quest_pos2.x, quest_pos2.y)
        # Draw Name
        rl.draw_text_ex(font, quest_name, rl.Vector2(pos.x, pos.y), text_font_size, spacing, color)
        name_size = rl.measure_text_ex(font, quest_name, text_font_size, spacing)
        pos.x += name_size.x + margin


def draw_journal(textures, tab_view: str, font: rl.Font, kills: dict, active_quests: dict, completed_quests: dict) -> str:
    rl.draw_texture_ex(textures["journal_pages"], rl.Vector2(journal_pos.x, journal_pos.y), 0, scale, rl.WHITE)
    tab_view = draw_tabs(textures, tab_view)
    if tab_view == "creatures":
        draw_creature(font, textures, "grass_tuft_weak", kills)

    if tab_view == "quests":
        draw_quests(font, active_quests, completed_quests)

    return tab_view

# list of monsters, draw 2 at a time, arrows move in the list
# if click tab button again or a back arrow somewhere, takes you to main list of every monster
# also return view
#   - "equips" "creatures" "list"
# if view == "list":
#   list_type = tab_view