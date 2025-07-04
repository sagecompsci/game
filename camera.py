import pyray as rl

true = True
false = False

drag = False

rl.init_window(800,800, "camera testing")

camera = rl.Camera2D
camera_x = 100
camera_y = 100
camera.target = rl.Vector2(camera_x,camera_y)
camera.offset = 1
camera.zoom = 3



while not rl.window_should_close():
    # if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
    #     drag = true
    rl.begin_drawing()
    rl.clear_background(rl.WHITE);
    for y in range(100):
        for x in range(100):
            if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
                color = rl.WHITE
            else:
                color = rl.BLACK
            rl.draw_rectangle(x * 50, y * 50, 50, 50, color)
    rl.end_drawing()

    if rl.is_key_pressed(rl.KeyboardKey.KEY_W):
        camera.target.x += 25
        # camera_x -= 25
        print(camera.target.x)





