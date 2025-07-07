import time
import random
from dataclasses import dataclass
import pyray as rl

true = True
false = False

rl.init_window(1900, 1000, "testing 3d camera")
rl.set_target_fps(60)


model = rl.load_model("models/grass.vox")
grass = rl.load_model("models/grass2.vox")
block = rl.load_model("models/grass_block.vox")


block_size = rl.get_model_bounding_box(block).max.x


camera = rl.Camera3D()
camera.position = rl.Vector3(0, 0, 0)  # camera position
camera.target = rl.Vector3(100, 0, 0)      # where camera is looking at
camera.up = rl.Vector3(0, 1 ,0)   # camera up vector(rotation towards target)
camera.fovy = 45        # camera field of view y

mouse_pos = rl.Vector2(rl.get_screen_width()/2, rl.get_screen_height()/2)

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
                model = block,
                position = rl.Vector3(pos_x, pos_y, pos_z)
            )

            models.append(block_model)

            chance = random.randint(1, 3)
            if chance == 1:
                grass_model = Model(
                    model = grass,
                    position = rl.Vector3(pos_x, pos_y + block_size, pos_z)
                )
                models.append(grass_model)

@dataclass
class Player:
    position: rl.Vector3
    falling: bool
    jumping: bool
    can_jump: bool
    height: int
    speed: float

player = Player(
    position = rl.Vector3(40, 10, 40),
    falling = false,
    jumping = false,
    can_jump = true,
    height = 10,
    speed = 1,
)

load_models(model_list)

def jump(player: Player):
    if rl.is_key_down(rl.KeyboardKey.KEY_SPACE) and player.can_jump:
        player.jumping = true
        player.can_jump = false

    if player.position.y >= player.height:
        player.jumping = false
        player.falling = true
    if player.position.y <= 0:
        player.falling = false
        player.can_jump = true

    if player.jumping:
        player.position.y += 1
    if player.falling:
        player.position.y -= 1
        if player.position.y <= 0:
            player.position.y = 0

def move(player: Player):
    if rl.is_key_down(rl.KeyboardKey.KEY_S):
        player.position.z += player.speed
        camera.target.y += player.speed/10
    if rl.is_key_down(rl.KeyboardKey.KEY_W):
        player.position.z -= player.speed
        camera.target.y -= player.speed/10
    if rl.is_key_down(rl.KeyboardKey.KEY_D):
        player.position.x += player.speed
        camera.target.x += player.speed
    if rl.is_key_down(rl.KeyboardKey.KEY_A):
        player.position.x -= player.speed
        camera.target.x -= player.speed

    camera.position = rl.Vector3(player.position.x, player.position.y + player.height,
                                 player.position.z)

def move_camera():
    current = rl.get_mouse_position()
    camera.target.y += mouse_pos.y - current.y
    camera.target.x += current.x - mouse_pos.x
    # im pretty sure i need to do something with camera.target.z, but i have no idea what, and this didn't work
    # if -2500 > camera.target.x > 2500:
    #     camera.target.z = 1000


    rl.set_mouse_position(int(mouse_pos.x), int(mouse_pos.y))


rl.set_mouse_position(int(mouse_pos.x), int(mouse_pos.y))

while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.WHITE)

    move(player)
    jump(player)
    move_camera()

    if rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
        rl.window_should_close()


    rl.begin_mode_3d(camera)
    for model in model_list:
        rl.draw_model(model.model, model.position, 1, rl.WHITE)

    rl.end_mode_3d()
    rl.end_drawing()