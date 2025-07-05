import time

import pyray as rl

rl.init_window(800, 800, "testing 3d camera")

camera = rl.Camera3D()
camera.position = rl.Vector3(0, 0, 5)  # camera position
camera.target = rl.Vector3(0, 0, 0)      # where camera is looking at
camera.up = rl.Vector3(0, 1 ,0)   # camera up vector(rotation towards target)
camera.fovy = 45        # camera field of view y

model = rl.load_model("models\grass.vox")

change_position = .005
change_target = .0005

def jump():
    for i in range (5):
        camera.position.y += 7
        time.sleep(.1)
        # start_time = time.time()
        # while time.time() - start_time < .5:
        #     pass

    # for i in range (5):
    #     camera.position.y -= 7
        # time.sleep(1)
        # start_time = time.time()
        # while time.time() - start_time < .5:
        #     pass


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

    if rl.is_key_pressed(rl.KeyboardKey.KEY_SPACE):
        jump()


    rl.begin_mode_3d(camera)
    if camera.position.z >= 0:
        rl.draw_model(model, rl.Vector3(0, 0, 0,), 1, rl.WHITE)

    rl.end_mode_3d()
    rl.end_drawing()