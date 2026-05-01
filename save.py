import pickle
import pyray as rl
from my_dataclasses import GameState, Tile, Building, InventoryItem


def save(state: GameState):
    with open(f"saves/{state.save}.pickle", "wb") as f:
        p = state.player
        player = (p.pos.x, p.pos.y, p.image, p.health, p.max_health, p.defense, p.strength, p.attack_speed, p.speed, p.last_attack)
        save_data = {
            "save": state.save,
            "player": player,
            "inventory": state.inventory,
            "gold": state.gold,
            "level": state.level,
            "view": state.view,
            "levels": state.levels,
            "buildings": state.buildings,
            "time": state.time,
        }
        pickle.dump([save_data], f, 2)

    print("saved")


def load(name: str, state: GameState):

    data = read_file(name)[0]
    state.save = data["save"]

    p = state.player
    p.pos.x, p.pos.y, p.image, p.health, p.max_health, p.defense, p.strength, p.attack_speed, p.speed, p.last_attack = \
    data["player"]

    state.inventory = data["inventory"]
    state.gold = data["gold"]

    state.level = data["level"]
    state.view = data["view"]
    state.levels = data["levels"]
    state.buildings = data["buildings"]
    state.time = data["time"]
    state.last_movement = state.time

    state.camera.target = rl.Vector2(state.player.pos.x, state.player.pos.y)



def read_file(name: str):
    with open(f"saves/{name}.pickle", "rb") as f:
        return pickle.load(f)
