import pyray as rl

true = True
false = False

drag = False

rl.init_window(800,800, "camera testing")

camera = rl.Camera2D()
camera_x = 0
camera_y = 0
camera.target = rl.Vector2(camera_x,camera_y)
camera.offset = rl.Vector2(-2500 + (rl.get_screen_width()/2), -2500 + (rl.get_screen_height()/2))
camera.zoom = 1



while not rl.window_should_close():
    # if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
    #     drag = true
    rl.begin_drawing()
    rl.clear_background(rl.WHITE);
    if rl.is_key_down(rl.KeyboardKey.KEY_W):
        camera.target.y -= 10
    if rl.is_key_down(rl.KeyboardKey.KEY_S):
        camera.target.y += 10
    if rl.is_key_down(rl.KeyboardKey.KEY_D):
        camera.target.x += 10
    if rl.is_key_down(rl.KeyboardKey.KEY_A):
        camera.target.x -= 10

    rl.begin_mode_2d(camera)
    for y in range(100):
        for x in range(100):
            if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
                color = rl.WHITE
            else:
                color = rl.BLACK
            rl.draw_rectangle(x * 50, y * 50, 50, 50, color)
    rl.end_drawing()
    rl.end_mode_2d()









