import pyray as rl
import os

# rl.init_window(800, 800, "fonts")

# font = rl.load_font_ex("font.ttf", 30, None, 0)
# font = rl.load_font_ex("LoveDays-2v7Oe.ttf", 30, None, 0)
font = rl.load_font_ex("font.ttf", 100, None, 0)
default = rl.get_font_default()
spacing = 1

# def wrap_lines(font: rl.Font, font_size: float, text: str, text_width: int) -> list[str]:
#     lines = []
#     text_size = rl.measure_text_ex(font, text, font_size, spacing)
#     if text_size.x > text_width:
#         words = text.split(" ")
#         line = []
#         while len(words) > 0:
#             if not line:
#                 line.append(words[0])
#                 words.pop(0)
#             else:
#                 while True:
#                     line.append(words[0])
#                     if rl.measure_text_ex(font, " ".join(line), font_size, spacing).x > text_width:
#                         line.pop(-1)
#                         lines.append(line.copy())
#                         line = []
#                         break
#
#                     else:
#                         words.pop(0)
#                         if len(words) <= 0:
#                             lines.append(line.copy())
#                             break
#
#     else:
#         lines = [text]
#
#     return lines

output = wrap_lines(font, 25, "This is a very long sentence that should hopefully be long enough to wrap "
                              "because I don't want to keep writing cause I've already written a lot.", 400)


for item in output:
    print(item)

# while not rl.window_should_close():
#
#     rl.begin_drawing()
#     rl.clear_background(rl.WHITE)
#
#
#     rl.draw_text_ex(font, "Hello World", (10, 10), 100, 10, rl.BLACK)
#     rl.draw_text_ex(font, "HELLO WORLD", (10, 100), 100, 10, rl.BLACK)
#
#     rl.end_drawing()
