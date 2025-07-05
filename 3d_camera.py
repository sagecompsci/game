import time
import random
from dataclasses import dataclass
import pyray as rl

true = True
false = False

rl.init_window(800, 800, "testing 3d camera")
rl.set_target_fps(60)


model = rl.load_model("models\grass.vox")
grass = rl.load_model("models\grass2.vox")
block = rl.load_model("models\grass_block.vox")


block_size = rl.get_model_bounding_box(block).max.x

camera = rl.Camera3D()
camera.position = rl.Vector3(0, 10, 40)  # camera position
camera.target = rl.Vector3(0, 0, 0)      # where camera is looking at
camera.up = rl.Vector3(0, 1 ,0)   # camera up vector(rotation towards target)
camera.fovy = 45        # camera field of view y


@dataclass
class Model:
    model: rl.Model
    position: rl.Vector3

model_list = []

def load_models(models: list[Model]):
    length = 30
    for i in range(length):
        for j in range(length):
            start = length // 2
            pos_y = 0
            pos_x = 0 + (j * block_size)
            pos_z = 0 + (i * block_size)

            block_model = Model(
                block,  # model
                rl.Vector3(pos_x, pos_y, pos_z) # position
            )

            models.append(block_model)

            chance = random.randint(1, 3)
            if chance == 1:
                grass_model = Model(
                    grass, # model
                    rl.Vector3(pos_x, pos_y + block_size, pos_z) # position
                )
                models.append(grass_model)



load_models(model_list)

change_position = 1
change_target = .1

jumping = false
can_jump = true
falling = false

while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.WHITE)
    if rl.is_key_down(rl.KeyboardKey.KEY_S):
        camera.position.z += change_position
        camera.target.y += change_target
    if rl.is_key_down(rl.KeyboardKey.KEY_W):
        camera.position.z -= change_position
        camera.target.y -= change_target
    if rl.is_key_down(rl.KeyboardKey.KEY_D):
        camera.position.x += change_position
        camera.target.x += change_position
    if rl.is_key_down(rl.KeyboardKey.KEY_A):
        camera.position.x -= change_position
        camera.target.x -= change_position

    if rl.is_key_down(rl.KeyboardKey.KEY_SPACE) and can_jump:
        jumping = true
        can_jump = false

    if camera.position.y >= 30:
        jumping = false
        falling = true
    if camera.position.y <= 10:
        falling = false
        can_jump = true


    if jumping:
        camera.position.y += 2
    if falling:
        camera.position.y -= 2
        if camera.position.y <= 10:
            camera.position.y = 10





    rl.begin_mode_3d(camera)
    for model in model_list:
        rl.draw_model(model.model, model.position, 1, rl.WHITE)



    # if camera.position.z >= 0:
    #     rl.draw_model(model, rl.Vector3(0, 0, 0,), 1, rl.WHITE)

    rl.end_mode_3d()
    rl.end_drawing()