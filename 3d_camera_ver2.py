import pyray as rl
import update_camera as uc
from dataclasses import dataclass


@dataclass
class GameState:
    models: dict[str: rl.Model]
    grass: rl.Model
    dirt: rl.Model
    block_size: float

    camera: rl.Camera3D
    test: rl.Camera3D

    can_jump: bool
    is_jumping: bool
    is_falling: bool
    height: float
    floor: float


def init() -> GameState:
    rl.init_window(1900, 1000, "3d camera v2")
    rl.set_target_fps(60)


    state = GameState (
        models = {},
        grass = rl.load_model("models/grass2.vox"),
        dirt = rl.load_model("models/grass_block.vox"),
        block_size = rl.get_model_bounding_box(self.dirt).max.x,



        camera = rl.Camera3D(),
        test = rl.Camera3D(),

        can_jump = True,
        is_jumping = False,
        is_falling = False,
        height =


    )





def main():
    state = init()


main()
