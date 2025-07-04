import pyray as rl

window_width = 800
window_height = 800
rl.init_window(window_width, window_height, "testing")
true = True
false = False


while not rl.window_should_close():
    rl.clear_background(rl.WHITE);
    rl.draw_rectangle(0,0,100,100, rl.PURPLE);
