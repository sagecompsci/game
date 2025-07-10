import random
from dataclasses import dataclass
import pyray as rl
import update_camera as c
true = True
false = False

rl.init_window(1900, 1000, "testing 3d camera")
rl.set_target_fps(60)


model = rl.load_model("models/grass.vox")
grass = rl.load_model("models/grass2.vox")
block = rl.load_model("models/grass_block.vox")

block_size = rl.get_model_bounding_box(block).max.x


def string_to_v3(string: str):
    data = string.split(",")
    return rl.Vector3(float(data[0]), float(data[1]), float(data[2]))

model_list = {}


def load_models(models: dict[rl.Vector3: rl.Model]):
    length = 30
    for i in range(length):
        for j in range(length):
            start_pos = 0 - ((length * block_size) // 2)
            pos_y = 0
            pos_x = start_pos + (j * block_size)
            if pos_x > 0:
                pos_y += block_size
            pos_z = start_pos + (i * block_size)

            models[f"{int(pos_x)},{int(pos_y)},{int(pos_z)}"] = block

            chance = random.randint(1, 3)
            if chance == 1:
                models[f"{int(pos_x)},{int(pos_y + block_size)},{int(pos_z)}"] = grass

@dataclass
class Player:
    position: rl.Vector3
    falling: bool
    jumping: bool
    can_jump: bool
    height: float
    jump_height: float
    speed: float
    floor: float

player = Player(
    position = rl.Vector3(0, 0, 0),
    falling = false,
    jumping = false,
    can_jump = true,
    height = block_size * 3,
    jump_height = block_size * 2.4,
    speed = 1,
    floor = block_size

)

camera = rl.Camera3D()
camera.position = rl.Vector3(0, player.height + player.floor, 0)  # camera position
camera.target = rl.Vector3(100, 0, 0)      # where camera is looking at
camera.up = rl.Vector3(0, 1 ,0)   # camera up vector(rotation towards target)
camera.fovy = 45        # camera field of view y

camera2 = rl.Camera3D()
camera2.position = rl.Vector3(0, player.height + player.floor, 0)  # camera position
camera2.target = rl.Vector3(100, 0, 0)      # where camera is looking at
camera2.up = rl.Vector3(0, 1 ,0)   # camera up vector(rotation towards target)
camera2.fovy = 45        # camera field of view y

load_models(model_list)



def jump(player: Player):
    if rl.is_key_down(rl.KeyboardKey.KEY_SPACE) and player.can_jump:
        player.jumping = true
        player.can_jump = false

    if camera.position.y >= player.height + player.jump_height + player.floor:
        player.jumping = false
        player.falling = true
    if camera.position.y <= player.height + player.floor:
        player.falling = false
        player.can_jump = true

    if player.jumping:
        camera.position.y += 1
    if player.falling:
        camera.position.y -= 1
        if camera.position.y <= player.height + player.floor:
            camera.position.y = player.height + player.floor


def update_position(player: Player, camera: rl.Camera3D):
    current = camera.position
    c.update_camera(camera, model_list, block_size)
    future = camera.position

    pos_x = camera.position.x // block_size
    pos_z = camera.position.z // block_size
    pos_y = (camera.position.y - (block_size * 4)) // block_size

    key = f"{int(pos_x)},{int(pos_y)},{int(pos_z)}"

    if key in model_list:
        if model_list[key] == block:
            player.floor = pos_y
        print(key)


    jump(player)


# def blocks_around(camera: rl.Camera3D, model: dict, block_size: float):
#     pos_x = camera.position.x // block_size
#     pos_z = camera.position.z // block_size
#     pos_y = (camera.position.y - (block_size * 4)) // block_size
#
#     key = f"{int(pos_x)},{int(pos_y + block_size)},{int(pos_z)}"
#     # print(f"key: {key}")
#
#     if key in model:
#         print("testing")

rl.hide_cursor()

rl.set_mouse_position(rl.get_screen_width()//2, rl.get_screen_height()//2)

while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.WHITE)

    update_position(player, camera2)
    camera = camera2

    # jump(player)
    #
    # c.update_camera(camera)
    rl.set_mouse_position(rl.get_screen_width() // 2, rl.get_screen_height() // 2)

    if rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
        rl.window_should_close()



    rl.begin_mode_3d(camera)
    for position, model in model_list.items():
        # print(position)
        position = string_to_v3(position)
        rl.draw_model(model, (position.x, position.y, position.z), 1, rl.WHITE)
        # print(f"position {position.x}, {position.y}, {position.z}")


    rl.draw_cube((0, block_size * 2 , 0), .1, .1, .1, rl.BLACK)

    rl.end_mode_3d()
    rl.end_drawing()