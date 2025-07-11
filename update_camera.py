import pyray as rl
import math

# def update_camera_pro(camera: rl.Camera3D, movement: rl.Vector3, rotation: rl.Vector3, zoom: float):
#     # Required values
#     # movement.x - Move forward/backward
#     # movement.y - Move right/left
#     # movement.z - Move up/down
#     # rotation.x - yaw
#     # rotation.y - pitch
#     # rotation.z - roll
#     # zoom - Move towards target
#
#     lock_view = True
#     rotate_around_target = False
#     rotate_up = False
#     move_in_world_plane = True
#
#     #Camera rotation
#     CameraPitch(camera, -rotation.y*DEG2RAD, lock_view, rotate_around_target, rotate_up);
#     CameraYaw(camera, -rotation.x*DEG2RAD, rotate_around_target);
#     CameraRoll(camera, rotation.z*DEG2RAD);
#
#     # Camera movement
#     CameraMoveForward(camera, movement.x, move_in_world_plane);
#     CameraMoveRight(camera, movement.y, move_in_world_plane);
#     CameraMoveUp(camera, movement.z);
#
#     # Zoom target distance
#     CameraMoveToTarget(camera, zoom);

def vector3_rotate_by_axis_angle(v: rl.Vector3, axis: rl.Vector3, angle: float):
    # Using Euler-Rodrigues Formula
    result = v

    # Vector3Normalize(axis);
    length = math.sqrt(axis.x*axis.x + axis.y*axis.y + axis.z*axis.z)
    if length == 0:
        length = 1

    i_length = 1/length
    axis.x *= i_length
    axis.y *= i_length
    axis.z *= i_length

    angle /= 2.0
    a = math.sin(angle)
    b = axis.x*a
    c = axis.y*a
    d = axis.z*a
    a = math.cos(angle)
    w = rl.Vector3(b, c, d)

    # Vector3CrossProduct(w, v)
    wv:rl.Vector3 = rl.Vector3(w.y*v.z - w.z*v.y, w.z*v.x - w.x*v.z, w.x*v.y - w.y*v.x)

    # Vector3CrossProduct(w, wv)
    wwv: rl.Vector3 = rl.Vector3(w.y*wv.z - w.z*wv.y, w.z*wv.x - w.x*wv.z, w.x*wv.y - w.y*wv.x)

    # Vector3Scale(wv, 2*a)
    a *= 2;
    wv.x *= a;
    wv.y *= a;
    wv.z *= a;

    # Vector3Scale(wwv, 2)
    wwv.x *= 2;
    wwv.y *= 2;
    wwv.z *= 2;

    result.x += wv.x;
    result.y += wv.y;
    result.z += wv.z;

    result.x += wwv.x;
    result.y += wwv.y;
    result.z += wwv.z;

    return result;

def vector3_scale(v: rl.Vector3, scalar: float):
    result: rl.Vector3 = rl.Vector3(v.x*scalar, v.y*scalar, v.z*scalar)
    return result

def vector3_add(v1: rl.Vector3, v2: rl.Vector3):
    result: rl.Vector3 = rl.Vector3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)
    return result

def vector3_normalize(v: rl.Vector3):
    result = v;

    length = math.sqrt(v.x*v.x + v.y*v.y + v.z*v.z);
    if length != 0:
        i_length = 1.0/length;

        result.x *= i_length;
        result.y *= i_length;
        result.z *= i_length;

    return result;

def vector3_subtract(v1: rl.Vector3, v2: rl.Vector3) -> rl.Vector3:
    result:rl.Vector3 = rl.Vector3(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)
    return result



def vector3_angle(v1: rl.Vector3, v2: rl.Vector3):
    result = 0
    cross: rl.Vector3 = rl.Vector3(v1.y*v2.z - v1.z*v2.y, v1.z*v2.x - v1.x*v2.z, v1.x*v2.y - v1.y*v2.x)
    length = math.sqrt(cross.x*cross.x + cross.y*cross.y + cross.z*cross.z)
    dot = (v1.x*v2.x + v1.y*v2.y + v1.z*v2.z)
    result = math.atan2(length, dot)

    return result;

def vector3_negate(v: rl.Vector3):
    result: rl.Vector3 = rl.Vector3(-v.x, -v.y, -v.z)
    return result;

def vector3_cross_product(v1: rl.Vector3, v2: rl.Vector3):
    result: rl.Vector3 = rl.Vector3(v1.y*v2.z - v1.z*v2.y, v1.z*v2.x - v1.x*v2.z, v1.x*v2.y - v1.y*v2.x)
    return result;

def get_camera_forward(camera: rl.Camera3D):
    return vector3_normalize(vector3_subtract(camera.target, camera.position))

def get_camera_right(camera: rl.Camera3D):
    forward = get_camera_forward(camera)
    up = get_camera_up(camera)
    return vector3_normalize(vector3_cross_product(forward, up))

def get_camera_up(camera: rl.Camera3D):
    return vector3_normalize(camera.up)

def camera_move_right(camera: rl.Camera3D, distance: float, move_in_world_plane: bool):
    right = get_camera_right(camera);

    if move_in_world_plane:
        # Project vector onto world plane
        right.y = 0;
        right = vector3_normalize(right);

    # Scale by distance
    right = vector3_scale(right, distance);

    # Move position and target
    camera.position = vector3_add(camera.position, right)
    camera.target = vector3_add(camera.target, right)


def camera_move_forward(camera: rl.Camera3D, distance: float, move_in_world_plane: bool):
    forward = get_camera_forward(camera)

    if move_in_world_plane:
        # Project vector onto world plane
        forward.y = 0;
        forward = vector3_normalize(forward)

    # Scale by distance
    forward = vector3_scale(forward, distance)

    # Move position and target
    camera.position = vector3_add(camera.position, forward)
    camera.target = vector3_add(camera.target, forward)


def update_camera(camera: rl.Camera3D):
    camera_move_speed = 1
    camera_rotation_speed = .03
    camera_pan_speed = .2
    camera_mouse_move_sensitivity = .003
    camera_orbital_speed = .5

    mouse_position_delta = rl.get_mouse_delta();

    move_in_world_plane = True
    rotate_around_target = False
    lock_view = True
    rotate_up = False

    # Camera speeds based on frame time
    camera_move_speed += rl.get_frame_time();
    camera_rotation_speed += rl.get_frame_time();
    camera_pan_speed *= rl.get_frame_time();
    camera_orbital_speed *= rl.get_frame_time();


    # Mouse support
    camera_yaw(camera, -mouse_position_delta.x*camera_mouse_move_sensitivity, rotate_around_target);
    camera_pitch(camera, -mouse_position_delta.y*camera_mouse_move_sensitivity, lock_view, rotate_around_target, rotate_up);



    # Keyboard support


    if rl.is_key_down(rl.KeyboardKey.KEY_W):
        camera_move_forward(camera, camera_move_speed, move_in_world_plane)
    if rl.is_key_down(rl.KeyboardKey.KEY_A):
        camera_move_right(camera, -camera_move_speed, move_in_world_plane)
    if rl.is_key_down(rl.KeyboardKey.KEY_S):
        camera_move_forward(camera, -camera_move_speed, move_in_world_plane)
    if rl.is_key_down(rl.KeyboardKey.KEY_D):
        camera_move_right(camera, camera_move_speed, move_in_world_plane)





def camera_yaw(camera: rl.Camera3D, angle: float, rotate_around_target: bool):
    # Rotation axis
    up = get_camera_up(camera)

    # View vector
    target_position:rl.Vector3 = vector3_subtract(camera.target, camera.position)

    # Rotate view vector around up axis
    target_position = vector3_rotate_by_axis_angle(target_position, up, angle)

    if rotate_around_target:
        # Move position relative to target
        camera.position = vector3_subtract(camera.target, target_position)

    else:
        # rotate around camera.position
        # Move target relative to position
        camera.target = vector3_add(camera.position, target_position)


def camera_pitch(camera: rl.Camera3D, angle: float, lock_view: bool, rotate_around_target: bool, rotate_up: bool):
    # Up direction
    up = get_camera_up(camera)

    # View vector
    target_position: rl.Vector3 = vector3_subtract(camera.target, camera.position)

    if lock_view:
        # In these camera modes we clamp the Pitch angle
        # to allow only viewing straight up or down.

        # Clamp view up
        max_angle_up = vector3_angle(up, target_position)
        max_angle_up -= 0 # avoid numerical errors
        if angle > max_angle_up:
            angle = max_angle_up

        # Clamp view down
        max_angle_down = vector3_angle(vector3_negate(up), target_position)
        max_angle_down *= -1 # downwards angle is negative
        max_angle_down += 0.001 # avoid numerical errors
        if angle < max_angle_down:
            angle = max_angle_down

    # Rotation axis
    right = get_camera_right(camera)

    # Rotate view vector around right axis
    target_position = vector3_rotate_by_axis_angle(target_position, right, angle);

    if rotate_around_target:
        # Move position relative to target
        camera.position = vector3_subtract(camera.target, target_position)
    else: # rotate around camera.position
        # Move target relative to position
        camera.target = vector3_add(camera.position, target_position)

    if rotate_up:
        # Rotate up direction around right axis
        camera.up = vector3_rotate_by_axis_angle(camera.up, right, angle);

























