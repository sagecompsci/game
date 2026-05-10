from classes.GameState import GameState
from information import views
from generate_levels.generate_one import create_level
from utilities.get_data import get_quest


def new_game(state: GameState) -> GameState:
    p = state.player
    p.health = 5
    p.max_health = 5
    p.strength = 1
    p.attack_speed = 1
    p.speed = 1

    state.view = views.game
    state.inventory_view = views.inventory_weapons
    state.journal_view = views.journal_creatures

    state.level = "one"
    state.location = "levels"

    level = state.levels["one"] = {}
    p.pos, level["tiles"], level["monsters"], level["chests"], state.buildings["one"] = create_level(state.tile_size, state.map_size)
    state.map = level

    state.quests[1] = get_quest(1)


    return state

