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

#create namedpipe to communicate with arduino simulator
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

# close pipe handle
def close_pipe_server(pipe):
    win32file.CloseHandle(pipe)

#write data through pipe
def write_pipe_server(pipe, data):
    data = str.encode(data)
    win32file.WriteFile(pipe, data)

#read data from pipe
def read_pipe_client():
    global pipe
    read_buffer = 64 * 1000
    result, dataRead = win32file.ReadFile(pipe, read_buffer, None)
    print("from pipe read: ", dataRead)
    #dataRead = ord(dataRead) - 48
    #dataRead=0
    return dataRead


# parse the keyboard input while beeing in the game_loop
def parse_events(vehicle, control):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYUP:
            if event.key == K_q:
                return True
    parse_vehicle_keys(pygame.key.get_pressed(), clock.get_time(), vehicle, control)

#parse vehicle control keys
def parse_vehicle_keys(keys, milliseconds, vehicle, control):
    #global steer_cache
    global pipe
    global flag_w
    global flag_s
    global flag_a
    global flag_d
    global motor
    global prevdata
    tosend_motor="0"
    tosend_stiring="0"
    global stiring
    
    if keys[K_UP] or keys[K_w]: #sends data through pipe while w or up is pressed
        motor=min(motor+1,512)
        flag_w = True
        print("w")

    else: #sends data once thorugh pipe if w or up is released
        if flag_w == True:
            motor=0
            print("w released")
            flag_w = False

    if keys[K_DOWN] or keys[K_s]: #sends data through pipe while w or up is pressed
        motor=600 #600 is code for brake, must a value not includet in the motor speed range
        flag_s = True
        print("s")

    else: #sends data once thorugh pipe if s or down is released
        if flag_s == True:
            motor=0
            print("s released")
            flag_s = False

    if keys[K_LEFT] or keys[K_a]: #sends data through pipe while a or left is pressed
        stiring = min(180, stiring + 1)
        flag_a = True
        print("a")

    else: #sends data once thorugh pipe if s or down is released
        if flag_a == True:
            stiring=90
            print("a released")
            flag_a = False

    if keys[K_RIGHT] or keys[K_d]:  # sends data through pipe while d or right is pressed
        stiring = max(0, stiring - 1)
        flag_d = True
        print("d")

    else:  # sends data once thorugh pipe if s or down is released
        if flag_d == True:
            stiring = 90
            print("d released")
            flag_d = False

    #tosend_motor=str(motor)
    data = outgoing_data_to_string(motor, stiring)
    #data=tosend_motor
    if prevdata!=data:
        print("data send: ",data)
        prevdata = data
        write_pipe_server(pipe, data)
        dataread=read_pipe_client()
        control_car(dataread)


def control_car(data):
    global control

    str_s=data[0]
    #int_s=str_s-48
    str_m=data[1]
    #int_m=str_m-48
    str_b=data[2]
    #int_b=str_b-48

    if str_s==49: #49 equals char 1
        #stiring
        #vehicle.apply_control(carla.VehicleControl(steer=(stiring-90)/120))
        control.steer=(stiring-90)/120
        print("carla steer: ", control.steer)

    if str_m==49:
        #throttle
        #vehicle.apply_control(carla.VehicleControl(throttle=motor/512))
        control.throttle=(motor/512)
        print("carla throttle: ", control.throttle)

    if str_b==49:
        #brake
        #vehicle.apply_control(carla.VehicleControl(hand_brake=1))
        control.brake=1
        print("carla brake on")
    elif str_b==48:
        #vehicle.apply_control(carla.VehicleControl(hand_brake=0))
        control.brake=0
        print("carla brake off")

    vehicle.apply_control(control)



def outgoing_data_to_string(int_m, int_s):
    str_m=str(int_m)
    str_m=str_m.zfill(3) #filling string up with zeros
    str_s=str(int_s)
    str_s = str_s.zfill(3)
    return str_m+','+str_s



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
    #steer_cache = 0
    attaching_camera()
    control = carla.VehicleControl()
    pipe = init_pipe_server()

    #flags für write function
    flag_w = False
    flag_s = False
    flag_a = False
    flag_d = False
    prevdata = "0"
    motor=0
    stiring=90
#------------------------------------------------main loop -----------------------------------------------------------
    while spielaktiv:
        clock.tick_busy_loop(60) #fps controll
        if parse_events(vehicle, control): #get keyboard events
            spielaktiv = False
        #control_pi(read_pipe_client(pipe))
        pygame.display.flip()


finally:
    close_pipe_server(pipe)
    print("destroying actors")
    for actor in actor_list:
        actor.destroy()