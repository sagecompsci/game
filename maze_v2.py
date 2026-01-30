# import pyray as rl
# from dataclasses import dataclass
# import random
#
#
# @dataclass
# class Tile:
#     pos: rl.Vector2
#     rotate_pos: rl.Vector2
#     rotation: int
#     texture: rl.Texture
#     tile: str
#     directions: list[str]
#
# @dataclass
# class GameState:
#     tile_size: int
#     maze_size: int
#     textures: dict
#     camera: rl.Camera2D
#
# def init():
#     rl.init_window(1800, 900, "Maze")
#     state = GameState(
#         tile_size= 40,
#         maze_size= 100,
#         textures = {},
#         camera = rl.Camera2D (),
#     )
#
#     state.camera.offset = rl.Vector2(0, 0)
#     state.camera.target = rl.Vector2(0, 0)
#     state.camera.rotation = 0
#     state.camera.zoom = 1
#
#     textures = [
#         "one",
#         "two",
#         "two_c",
#         "three",
#         "four",
#         "none",
#     ]
#
#     for texture in textures:
#         state.textures[texture] = rl.load_texture(f"images/{texture}.png")
#
#     return state
#
# def str_v2(string: str) -> rl.Vector2:
#     x, y = string.split(",")
#     return rl.Vector2(int(x), int(y))
#
# def v2_str(v2: rl.Vector2) -> str:
#     return f"{v2.x},{v2.y}"
#
# def rotate(state: GameState, pos: rl.Vector2, rotation: int) -> rl.Vector2:
#     if rotation == 90:
#         pos.x += state.tile_size
#     elif rotation == 180:
#         pos.y += state.tile_size
#         pos.x += state.tile_size
#     elif rotation == 270:
#         pos.y += state.tile_size
#
#     return pos
#
# def get_opposite_direction(direction: str) -> str:
#     opposite = ""
#     if direction == "north":
#         opposite = "south"
#     elif direction == "south":
#         opposite = "north"
#     elif direction == "west":
#         opposite = "east"
#     elif direction == "east":
#         opposite = "west"
#     return opposite
#
# def get_tile(directions: list[str]) -> str:
#     tile = "none"
#     if len(directions) == 1:
#         tile = "one"
#     elif len(directions) == 2:
#         if directions[0] == get_opposite_direction(directions[1]):
#             tile = "two"
#         else:
#             tile = "two_c"
#
#     elif len(directions) == 3:
#         tile = "three"
#     elif len(directions) == 4:
#         tile = "four"
#
#     return tile
#
# def get_rotation(tile: str, directions: list[str]) -> int:
#     rotation = 0
#     if tile == "one":
#         if "east" in directions:
#             rotation = 90
#         elif "south" in directions:
#             rotation = 180
#         elif "west" in directions:
#             rotation = 270
#
#     elif tile == "two":
#         if "east" in directions:
#             rotation = 90
#
#     elif tile == "two_c":
#         if "south" in directions:
#             rotation = 90
#             if "west" in directions:
#                 rotation += 90
#         elif "north" in directions and "west" in directions:
#             rotation = 270
#
#     elif tile == "three":
#         if not "west" in directions:
#             rotation = 90
#         elif not "north" in directions:
#             rotation = 180
#         elif not "east" in directions:
#             rotation = 270
#
#     return rotation
#
# def get_directions(state: GameState, maze: dict, pos: rl.Vector2) -> list[str]:
#     directions = []
#     possible_directions = []
#     for i in range(4):
#         pos2 = rl.Vector2(pos.x, pos.y)
#         direction = ""
#         if i == 0:
#             pos2.x += state.tile_size
#             direction = "east"
#         elif i == 1:
#             pos2.x -= state.tile_size
#             direction = "west"
#         elif i == 2:
#             pos2.y += state.tile_size
#             direction = "south"
#         elif i == 3:
#             pos2.y -= state.tile_size
#             direction = "north"
#
#         pos2_str = v2_str(rl.Vector2(pos2.x, pos2.y))
#         if pos2_str in maze.keys():
#             opposite = get_opposite_direction(direction)
#             if opposite in maze[pos2_str].directions:
#                 directions.append(direction)
#
#         elif 0 <= pos2.x <= (state.maze_size*state.tile_size) - state.tile_size and 0 <= pos2.y <= (state.maze_size*state.tile_size) - state.tile_size:
#             num = random.randint(1, 2)
#             if num == 1:
#                 directions.append(direction)
#             # if num == 2:
#             #     possible_directions.append(direction)
#
#         if i == 3 and len(directions) == 0:
#             if len(possible_directions) > 0:
#                 directions.append(possible_directions[0])
#
#     return directions
#
# def create_tile(state: GameState, maze: dict, pos: rl.Vector2, directions: list[str] = None) -> Tile:
#     if directions is None:
#         directions = get_directions(state, maze, pos)
#
#     tile = get_tile(directions)
#     rotation = get_rotation(tile, directions)
#     rotate_pos = rotate(state, rl.Vector2(pos.x, pos.y), rotation)
#     texture = state.textures[tile]
#
#
#     return Tile (
#         pos = pos,
#         rotate_pos = rotate_pos,
#         rotation = rotation,
#         texture = texture,
#         tile = tile,
#         directions = directions,
#     )
#
# def create_maze(state: GameState) -> dict:
#     maze = {}
#     for y in range(state.maze_size):
#         for x in range(state.maze_size):
#             tile = create_tile(state, maze, pos = rl.Vector2(x * state.tile_size, y * state.tile_size))
#
#             string = v2_str(tile.pos)
#             maze[string] = tile
#
#
#     return maze
#
# def pos_from_direction(state: GameState, direction: str, pos: rl.Vector2) -> rl.Vector2:
#     pos2 = rl.Vector2(pos.x, pos.y)
#     if direction == "north":
#         pos2.y -= state.tile_size
#     elif direction == "south":
#         pos2.y += state.tile_size
#     elif direction == "east":
#         pos2.x += state.tile_size
#     elif direction == "west":
#         pos2.x -= state.tile_size
#
#     return pos2
#
# def is_adjacent(state: GameState, pos: rl.Vector2, pos2: rl.Vector2) -> bool:
#     x_diff = pos.x - pos2.x
#     y_diff = pos.y - pos2.y
#     if (x_diff == -state.tile_size or x_diff == state.tile_size) and y_diff == 0:
#             return True
#     elif (y_diff == -state.tile_size or y_diff == state.tile_size) and x_diff == 0:
#             return True
#
#     return False
#
#
# def get_path(state: GameState, maze2: dict, path: list[rl.Vector2], tile: Tile) -> list[rl.Vector2]:
#     for direction in tile.directions:
#         pos = pos_from_direction(state, direction, rl.Vector2(tile.pos.x, tile.pos.y))
#         key = v2_str(rl.Vector2(pos.x, pos.y))
#
#         if key in maze2.keys():
#             path.append(rl.Vector2(pos.x, pos.y))
#             new_tile = maze2[key]
#             maze2.pop(key)
#             path = get_path(state, maze2, path, new_tile)
#
#
#     return path
#
# def get_paths(state: GameState, maze: dict) -> list[list[rl.Vector2]]:
#     paths = []
#     maze2 = {}
#     for key, value in maze.items():
#         maze2[key] = value
#     while len(maze2) > 0:
#         key = list(maze2)[0]
#         tile = maze2[key]
#         maze2.pop(key)
#         path = get_path(state, maze2, [rl.Vector2(tile.pos.x, tile.pos.y)], tile)
#         paths.append(path)
#
#     return paths
#
# def recreate_maze(state: GameState, maze: dict) -> dict:
#     paths = get_paths(state, maze)
#     for path in paths:
#         for pos in path:
#             for path2 in paths:
#                 if not pos in path2:
#                     for pos2 in path2:
#                         if is_adjacent(state, rl.Vector2(pos.x, pos.y), rl.Vector2(pos2.x, pos2.y)):
#                             direction = ""
#                             if pos.x - pos2.x == state.tile_size:
#                                 direction = "west"
#                             elif pos.x - pos2.x == -state.tile_size:
#                                 direction = "east"
#                             elif pos.y - pos2.y == state.tile_size:
#                                 direction = "north"
#                             elif pos.y - pos2.y == -state.tile_size:
#                                 direction = "south"
#
#                             opposite = get_opposite_direction(direction)
#
#                             key1 = v2_str(rl.Vector2(pos.x, pos.y))
#                             key2 = v2_str(rl.Vector2(pos2.x, pos2.y))
#
#                             maze[key1].directions.append(direction)
#                             maze[key2].directions.append(opposite)
#                             maze[key1] = create_tile(state, maze, rl.Vector2(pos.x, pos.y), maze[key1].directions)
#                             maze[key2] = create_tile(state, maze, rl.Vector2(pos2.x, pos2.y), maze[key2].directions)
#
#                             break
#                     else:
#                         continue
#                     break
#                 else:
#                     break
#             else:
#                 continue
#             break
#
#     return maze
#
# def draw_maze(state: GameState, maze: dict):
#     for tile in maze.values():
#         rl.draw_texture_ex(tile.texture, tile.rotate_pos, tile.rotation, state.tile_size // 8, rl.WHITE)
#
# def main():
#     state = init()
#     maze = create_maze(state)
#     recreate_maze(state, maze)
#
#     while not rl.window_should_close():
#         speed = 1
#         if rl.is_key_down(rl.KeyboardKey.KEY_W):
#             state.camera.target.y -= speed
#         if rl.is_key_down(rl.KeyboardKey.KEY_S):
#             state.camera.target.y += speed
#         if rl.is_key_down(rl.KeyboardKey.KEY_D):
#             state.camera.target.x += speed
#         if rl.is_key_down(rl.KeyboardKey.KEY_A):
#             state.camera.target.x -= speed
#         if rl.is_key_pressed(rl.KeyboardKey.KEY_Z):
#             state.camera.zoom += 1
#         if rl.is_key_pressed(rl.KeyboardKey.KEY_X):
#             state.camera.zoom -= 1
#
#
#         rl.begin_drawing()
#         rl.clear_background(rl.WHITE)
#         rl.begin_mode_2d(state.camera)
#         draw_maze(state, maze)
#
#         rl.end_mode_2d()
#         rl.end_drawing()
#
# main()