import pyray as rl
import update_camera as c
from dataclasses import dataclass


@dataclass
class GameState:
    models: dict[str: rl.Model]
    dirt: rl.Model
    block_size: float

    camera: rl.Camera3D
    test: rl.Camera3D

    can_jump: bool
    is_jumping: bool
    is_falling: bool
    height: float
    jump_height: float
    floor: float


def init() -> GameState:
    rl.init_window(1900, 1000, "3d camera v2")
    rl.set_target_fps(60)
    grass = rl.load_model("models/grass2.vox")
    dirt = rl.load_model("models/grass_block.vox")
    block_size = float(rl.get_model_bounding_box(dirt).max.x)

    state = GameState (
        models = {},
        dirt = dirt,
        block_size = block_size,

        camera = rl.Camera3D(),
        test = rl.Camera3D(),

        can_jump = True,
        is_jumping = False,
        is_falling = False,
        height = block_size * 2,
        jump_height = block_size * 3,
        floor = block_size,
    )

    state.camera.position = rl.Vector3(0, state.height + state.floor , 1,)
    state.camera.target = rl.Vector3(0, 5, 0)
    state.camera.up = rl.Vector3(0, 1, 0)
    state.camera.fovy = 45

    state.test = state.camera


    return state

def vector3_to_string(v: rl.Vector3) -> str:
    return f"{v.x},{v.y},{v.z}"

def string_to_vector3(s: str) -> rl.Vector3:
    s = s.split(',')
    return rl.Vector3(float(s[0]), float(s[1]), float(s[2]))

def load_models(state: GameState):
    length = 50
    for i in range(length):
        for j in range(length):
            start = 0 - ((length * state.block_size) // 2)
            pos_x = start + (j * state.block_size)
            pos_z = start + (i * state.block_size)
            pos_y = 0

            key = vector3_to_string(rl.Vector3(pos_x, pos_y, pos_z))
            state.models[key] = state.dirt

            if pos_x < -5:
                pos_y = state.block_size
                key = vector3_to_string(rl.Vector3(pos_x, pos_y, pos_z))
                state.models[key] = state.dirt



def draw_models(state: GameState):
    for position, model in state.models.items():
        rl.draw_model(model, string_to_vector3(position), 1, rl.WHITE)

def jump(state: GameState):
    if rl.is_key_down(rl.KeyboardKey.KEY_SPACE) and state.can_jump:
        state.is_jumping = True
        state.can_jump = False

    ceiling = state.jump_height + state.floor + state.height
    floor = state.floor + state.height

    # if not state.is_jumping:
    #     if state.test.position.y < state.height + state.floor:
    #         state.is_falling = True
    #         state.can_jump = False

    if state.is_jumping:
        if state.test.position.y < ceiling:
            state.test.position.y += .5
            state.test.target.y += .5
        if state.test.position.y >= ceiling:
            state.test.position.y = ceiling
            state.is_jumping = False
            state.is_falling = True

    if state.is_falling:
        state.test.position.y -= .5
        state.test.target.y -= .5
        if state.test.position.y <= floor:
            state.test.position.y = floor
            state.is_falling = False
            state.can_jump = True




def update_movement(state: GameState):
    jump(state)
    c.update_camera(state.test)

    test = state.test.position
    pos_x = (test.x // state.block_size) * state.block_size
    pos_y = ((test.y - state.height - state.floor) // state.block_size) * state.block_size
    pos_z = (test.z // state.block_size) * state.block_size

    key = vector3_to_string(rl.Vector3(pos_x, pos_y + state.block_size, pos_z))
    if key in state.models:
        print("not walking")

    else:
        print("walking")
        state.camera = state.test

    key = vector3_to_string(rl.Vector3(pos_x, pos_y, pos_z))
    # print(key)

    if key in state.models:
        if state.models[key] == state.dirt:
            state.floor = pos_y + state.block_size
    elif not state.is_jumping:
        state.is_falling = True







def main():
    state = init()
    load_models(state)
    rl.hide_cursor()

    rl.set_mouse_position(rl.get_screen_width()//2, rl.get_screen_height()//2)

    while not rl.window_should_close():
        if rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
            rl.window_should_close()

        rl.begin_drawing()
        rl.clear_background(rl.WHITE)

        # c.update_camera(state.camera)
        update_movement(state)
        rl.set_mouse_position(rl.get_screen_width() // 2, rl.get_screen_height() // 2)

        rl.begin_mode_3d(state.camera)

        # rl.draw_model(state.dirt, (0, 0, 0), 1, rl.WHITE)

        draw_models(state)


        rl.end_mode_3d()
        rl.end_drawing()


main()
