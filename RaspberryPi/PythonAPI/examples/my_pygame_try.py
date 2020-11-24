import time
try:
    import pygame
    from pygame.locals import KMOD_CTRL
    from pygame.locals import KMOD_SHIFT
    from pygame.locals import K_0
    from pygame.locals import K_9
    from pygame.locals import K_BACKQUOTE
    from pygame.locals import K_BACKSPACE
    from pygame.locals import K_COMMA
    from pygame.locals import K_DOWN
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_F1
    from pygame.locals import K_LEFT
    from pygame.locals import K_PERIOD
    from pygame.locals import K_RIGHT
    from pygame.locals import K_SLASH
    from pygame.locals import K_SPACE
    from pygame.locals import K_TAB
    from pygame.locals import K_UP
    from pygame.locals import K_a
    from pygame.locals import K_c
    from pygame.locals import K_g
    from pygame.locals import K_d
    from pygame.locals import K_h
    from pygame.locals import K_m
    from pygame.locals import K_n
    from pygame.locals import K_p
    from pygame.locals import K_q
    from pygame.locals import K_r
    from pygame.locals import K_s
    from pygame.locals import K_w
    from pygame.locals import K_l
    from pygame.locals import K_i
    from pygame.locals import K_z
    from pygame.locals import K_x
    from pygame.locals import K_MINUS
    from pygame.locals import K_EQUALS
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')



import glob
import os
import sys
import win32file, win32pipe, pywintypes

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
import random
import numpy as np

# -------------------------------------------------------functions-------------------------------------------------------


def init_pipe_server():
    pipe = win32pipe.CreateNamedPipe(
        r'\\.\\pipe\\MYNAMEDPIPE',
        win32pipe.PIPE_ACCESS_DUPLEX,
        # win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE,
        1, 65536, 65536,
        0,
        None)
    try:
        print("Waiting for Communication: Pipe Client: Arduino")
        win32pipe.ConnectNamedPipe(pipe, None)
        print("Communication accessed: got Pipe Client: connected to Arduino")
    except:
        print("Connection to pipe client: arduino failed")
        return False

    return pipe


def close_pipe_server(pipe):
    win32file.CloseHandle(pipe)


def write_pipe_server(pipe, data):
    data = str.encode(data)
    win32file.WriteFile(pipe, data)


def read_pipe_client():
    global pipe
    read_buffer = 64 * 1000
    result, dataRead = win32file.ReadFile(pipe, read_buffer, None)
    print(dataRead)
    dataRead = ord(dataRead) - 48
    return dataRead


# parse the keyboard input while beeing in the game_loop

def control_pi(value):
    vehicle.apply_control(carla.VehicleControl(throttle=value))

def parse_events(vehicle, control):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYUP:
            if event.key == K_q:
                return True

    parse_vehicle_keys(pygame.key.get_pressed(), clock.get_time(), vehicle, control)

# parse the keyboard input for driving the car while beeing in the game_loop
'''
this functions works well, commented for trying other parse_vehicle_key function with pipe communication
def parse_vehicle_keys(keys, milliseconds, vehicle, control): #fehlerhaft bei throttles
    global steer_cache

    if keys[K_UP] or keys[K_w]:
        vehicle.apply_control(carla.VehicleControl(throttle=1.0))
        #vehicle.throttle = min(vehicle.throttle + 0.01, 1)
        #carla.VehicleControl.throttle = 1
        #print(control.throttle)
        print("w")
    else:
        vehicle.apply_control(carla.VehicleControl(throttle=0.0))
        #vehicle.throttle = 0

    if keys[K_DOWN] or keys[K_s]:
        print("s")
        #control.throttle = max(control.throttle -0.01, -1)
        vehicle.apply_control(carla.VehicleControl(brake=1))

    steer_increment = 5e-4 * milliseconds
    if keys[K_RIGHT] or keys[K_d]:
        if steer_cache > 0:
            steer_cache = 0
        else:
            steer_cache -= steer_increment

        vehicle.apply_control(carla.VehicleControl(steer=steer_cache))

    if keys[K_LEFT] or keys[K_a]:
        if steer_cache < 0:
            steer_cache = 0
        else:
            steer_cache += steer_increment

        vehicle.apply_control(carla.VehicleControl(steer=steer_cache))

    print(steer_cache)
    #control.steer = steer_cache
'''

def parse_vehicle_keys(keys, milliseconds, vehicle, control): #fehlerhaft bei throttles
    global steer_cache
    global pipe
    global flag_w
    global flag_s

    if keys[K_UP] or keys[K_w]:
        #vehicle.apply_control(carla.VehicleControl(throttle=1.0))
        data = "m1"
        write_pipe_server(pipe, str(data))
        control_pi(read_pipe_client())
        #read_pipe_client()
        flag_w = True
        print("w")

    else:
        if flag_w == True:
            #vehicle.apply_control(carla.VehicleControl(throttle=0.0))
            data = "m0"
            write_pipe_server(pipe, str(data))
            control_pi(read_pipe_client())
            #read_pipe_client()
            print("s")
            flag_w = False



    if keys[K_DOWN] or keys[K_s]:
        print("s")
        #control.throttle = max(control.throttle -0.01, -1)
        #vehicle.apply_control(carla.VehicleControl(brake=1))
        flag_s = True
        data = "b1"
        write_pipe_server(pipe, data)
    else:
        if flag_s == True:
            data = "b0"
            write_pipe_server(pipe, data)
            flag_s = False


    steer_increment = 5e-4 * milliseconds
    if keys[K_RIGHT] or keys[K_d]:
        if steer_cache > 0:
            steer_cache = 0
        else:
            steer_cache -= steer_increment

        data = "r"+str(max(steer_cache, 1))
        write_pipe_server(pipe, data)
        #vehicle.apply_control(carla.VehicleControl(steer=steer_cache))

    if keys[K_LEFT] or keys[K_a]:
        if steer_cache < 0:
            steer_cache = 0
        else:
            steer_cache += steer_increment
        data = "r" + str(min(steer_cache, 1))
        write_pipe_server(pipe, data)
        #vehicle.apply_control(carla.VehicleControl(steer=steer_cache))

    #print(steer_cache)
    #control.steer = steer_cache

    #data = str(mforward) + "," + str(mbrake) + "," + str(steer_cache) + ","





def image(data):
    i = np.array(data.raw_data)  # convert to an array
    i2 = i.reshape((480, 680, 4))
    i3 = i2[:, :, :3]
    i3 = np.rot90(i3)
    i4 = pygame.surfarray.make_surface(i3)
    display.blit(i4, (0, 0))


def attaching_camera():
    bp_cam = blueprint_library.find('sensor.camera.rgb')
    # changing image dimesnions
    bp_cam.set_attribute('image_size_x', f'{680}')
    bp_cam.set_attribute('image_size_y', f'{480}')
    bp_cam.set_attribute('fov', '110')
    # adding the camera to the car
    spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    sensor = world.spawn_actor(bp_cam, spawn_point, attach_to=vehicle)
    # add to actors list
    actor_list.append(sensor)

    # get the camera data
    sensor.listen(lambda data: image(data))

#--------------------------------------------------------beginning------------------------------------------------------
try:
    pygame.init()
    actor_list = []
    # connecting to our server
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    world = client.get_world()

    blueprint_library = world.get_blueprint_library()
    # filter for tesla model3  in blueprints
    bp = blueprint_library.filter('model3')[0]

    # choose a random spwanpoint
    spawn_point = random.choice(world.get_map().get_spawn_points())
    vehicle = world.spawn_actor(bp, spawn_point)
    # add vehicle to actr list
    actor_list.append(vehicle)

    # pygame
    display = pygame.display.set_mode((680,480), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("first game try amk")

    clock = pygame.time.Clock()
    spielaktiv = True
    steer_cache = 0
    attaching_camera()
    control = carla.VehicleControl()
    pipe = init_pipe_server()

    #flags für write function
    flag_w = False
    flag_s = False

    while spielaktiv:
        clock.tick_busy_loop(60)
        if parse_events(vehicle, control):
            spielaktiv = False
        #control_pi(read_pipe_client(pipe))
        pygame.display.flip()


finally:
    close_pipe_server(pipe)
    print("destroying actors")
    for actor in actor_list:
        actor.destroy()
