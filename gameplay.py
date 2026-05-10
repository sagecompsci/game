import pyray as rl
from classes.GameState import GameState
from movement import update_movement

def gameplay(state: GameState):

    p = state.player

    # movement.open_chest(state.inventory, state.view, p.pos)
    # movement.fight_monster(state.inventory, p, state.view["monsters"], state.view, state.tile_size, state.time,
    #                        state.kills, state.quests["active"], state.all_quests)


    if state.time - state.last_movement > p.speed * 10:
        state.last_movement = state.time
        state.map, state.location = update_movement(p, state.map, state.buildings, state.levels, state.level, state.location, state.tile_size)
        # keep track of last time of movement, if greater than 7 then walk

    state.camera.target = rl.Vector2(p.pos.x, p.pos.y)
