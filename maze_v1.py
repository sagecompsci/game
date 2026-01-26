import pyray as rl
import random
from dataclasses import dataclass

size = 80

camera = rl.Camera2D()
camera.target = rl.Vector2(rl.get_screen_width()//2,rl.get_screen_height()//2)
camera.offset = rl.Vector2(rl.get_screen_width()//2,rl.get_screen_height()//2)
camera.zoom = 1

@dataclass
class Path:
    pos: rl.Vector2
    texture: rl.Texture
    tile: str
    rotation: float
    directions: list[str]


def v2_in_list(v2: rl.Vector2, items: list[Path]):
    for i in range(len(items)):
        if v2.x == items[i].pos.x and v2.y == items[i].pos.y:
            return True
    return False

def get_opposite_dir(direction: str) -> str:
    opposite = ""
    if direction == "north":
        opposite = "south"
    if direction == "south":
        opposite = "north"
    if direction == "east":
        opposite = "west"
    if direction == "west":
        opposite = "east"

    return opposite


def get_new_pos(direction: str, pos: rl.Vector2) -> rl.Vector2:
    pos2 = rl.Vector2(pos.x, pos.y)
    if direction == "north":
        pos2.y += 1 * size
    elif direction == "south":
        pos2.y -= 1 * size
    elif direction == "east":
        pos2.x -= 1 * size
    elif direction == "west":
        pos2.x += 1 * size

    return pos2

def get_base_rotation(direction) -> float:
    rotation = 0
    if direction == "east":
        rotation = 90
    elif direction == "south":
        rotation = 180
    elif direction == "west":
        rotation = -90
    return rotation

def should_end(path: Path) -> bool:
    if path.directions[0] == path.directions[1]:
        return True
    return False

def get_start():
    start = rl.Vector2(0, 0)
    start.x = ((rl.get_screen_width()//2)//size) * size
    start.y = ((rl.get_screen_height()//2)//size) * size
    return start

def get_path(path: list[Path], pos: rl.Vector2, tile: str = "") -> Path:
    directions = []

    if len(path) == 0:
        tile = "one"
        options = ["north", "east", "west", "south"]
        direction1 = random.choice(options)

    else:
        if tile == "":
            tiles = ["one", "two", "two_c"]
            if len(path) < 10:
                tiles.remove("one")
            if path[-1].tile == "two_c" and path[-1].tile == "two_c":
                tiles.remove("two_c")
            tile = random.choice(tiles)

        direction1 = get_opposite_dir(path[-1].directions[1])


    texture = rl.load_texture(f"images/{tile}.png")

    directions.append(direction1)

    rotation = get_base_rotation(direction1)

    if tile == "one":
        directions.append(direction1)

    elif tile == "two":
        direction2 = get_opposite_dir(direction1)
        directions.append(direction2)

    elif tile == "two_c":
        rotation = 0
        options = ["north", "east", "south", "west"]
        opposite = get_opposite_dir(direction1)

        options.remove(direction1)
        options.remove(opposite)

        index = random.randint(0, 1)

        direction2 = options[index]
        directions.append(direction2)

        if "south" in directions:
            rotation = 90
            if "west" in directions:
                rotation += 90
        elif "north" in directions and "west" in directions:
            rotation = -90


    pos2 = rl.Vector2(pos.x, pos.y)

    if rotation == 90:
        pos2.x += size
    elif rotation == 180:
        pos2.y += size
        pos2.x += size
    elif rotation == -90:
        pos2.y += size


    new_path =  Path (
        pos = rl.Vector2(pos2.x, pos2.y),
        texture = texture,
        tile = tile,
        rotation = rotation,
        directions = directions
    )

    if len(path) > 0 and tile != "one":
        new_pos = get_new_pos(get_opposite_dir(directions[-1]), rl.Vector2(pos.x, pos.y))
        if v2_in_list(new_pos, path):
            new_path = get_path(path, rl.Vector2(pos.x, pos.y), tile = "one")




    return new_path



def create_line(path: list[Path], pos: rl.Vector2) -> list[Path]:
    if len(path) == 0:
        path.append(get_path(path, rl.Vector2(pos.x, pos.y)))

    direction = get_opposite_dir(path[-1].directions[1])

    pos2 = get_new_pos(direction, rl.Vector2(pos.x, pos.y))

    tile = get_path(path, pos2)
    path.append(tile)
    if should_end(path[-1]):
        for i in range(len(path)):
            print(f"{path[i].tile} {path[i].pos.x}, {path[i].pos.y}  {path[i].directions[0]} {path[i].directions[1]} {path[i].rotation}")
        return path

    return create_line(path, pos2)


def draw_line(path: list[Path]):
    for i in range(len(path)):
        tile = path[i]
        rl.draw_texture_ex(tile.texture, rl.Vector2(tile.pos.x, tile.pos.y), tile.rotation, size//8, rl.WHITE)
        if i == 0:
            rl.draw_rectangle(int(tile.pos.x), int(tile.pos.y), 10, 10, rl.PINK)

def test_draw():
    test = rl.load_texture("images/one.png")
    pos = rl.Vector2(0, 0)
    rotation = 270
    if rotation == 90:
        pos.x += size
    elif rotation == 180:
        pos.y += size
        pos.x += size
    elif rotation == 270:
        pos.y += size
    rl.draw_texture_ex(test, rl.Vector2(pos.x, pos.y), rotation , size//8, rl.WHITE)
    print(f"pos: {pos.x}, {pos.y}")


def main():
    rl.init_window(800, 800, "hello")
    start = get_start()
    path = create_line([], start)

    while not rl.window_should_close():
        if rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
            rl.window_should_close()

        rl.begin_drawing()
        rl.clear_background(rl.WHITE)
        if rl.is_key_down(rl.KeyboardKey.KEY_W):
            camera.target.y -= .1
        if rl.is_key_down(rl.KeyboardKey.KEY_S):
            camera.target.y += .1
        if rl.is_key_down(rl.KeyboardKey.KEY_D):
            camera.target.x += .1
        if rl.is_key_down(rl.KeyboardKey.KEY_A):
            camera.target.x -= .1
        if rl.is_key_pressed(rl.KeyboardKey.KEY_Z):
            camera.zoom += 1

        rl.begin_mode_2d(camera)
        draw_line(path)
        # test_draw()
        rl.end_mode_2d()
        rl.end_drawing()

main()