#wie raspberrypi_Car_1 nur dass hier mit klassen gearbeitet wird.

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



#--------------------------------------------------class camera manager------------------------------------------------
class camera(object):
    def __init__(self, world):
        global actor_list

    def image(self, data):
        #cc = carla.ColorConverter.CityScapesPalette
        #data.convert(cc) nur für semantic segmentation camera
        i = np.array(data.raw_data)  # convert to an array
        i2 = i.reshape((480, 680, 4))
        i3 = i2[:, :, :3]
        i3 = np.rot90(i3)
        i4 = pygame.surfarray.make_surface(i3)
        display.blit(i4, (0, 0))

    def attaching_camera(self):
        #bp_cam = blueprint_library.find('sensor.camera.semantic_segmentation')
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
        sensor.listen(lambda data: self.image(data))

#--------------------------------------------------class keyboard-------------------------------------------------------
class keyboard(object):
    def __init__(self, world):
        self._control = carla.VehicleControl()
        #player = world.player
        # flags für write function
        self._flag_w = False
        self._flag_s = False
        self._flag_a = False
        self._flag_d = False
        self._prevdata = "0"
        self._motor = 0
        self._stiring = 90

    # parse the keyboard input while beeing in the game_loop
    def parse_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYUP:
                if event.key == K_q:
                    return True
        self.parse_vehicle_keys(pygame.key.get_pressed(), clock.get_time())

    #todo: boolean return statements for debugging
    def parse_vehicle_keys(self, keys, milliseconds):
        #tosend_motor = "0"
        #tosend_stiring = "0"

        if keys[K_UP] or keys[K_w]:  # sends data through pipe while w or up is pressed
            self._control.throttle = min(self._control.throttle + 1, 512)
            self._flag_w = True
            print("w")

        else:  # sends data once thorugh pipe if w or up is released
            if self._flag_w == True:
                self._control.throttle = 0
                print("w released")
                self._flag_w = False

        if keys[K_DOWN] or keys[K_s]:  # sends data through pipe while w or up is pressed
            self._control.brake = 1  # 600 is code for brake, must a value not includet in the motor speed range
            self._flag_s = True
            print("s")

        else:  # sends data once thorugh pipe if s or down is released
            if self._flag_s == True:
                self._control.brake = 0
                print("s released")
                self._flag_s = False

        if keys[K_LEFT] or keys[K_a]:  # sends data through pipe while a or left is pressed
            self._stiring = min(180, self._stiring + 1)
            self._flag_a = True
            print("a")

        else:  # sends data once thorugh pipe if s or down is released
            if self._flag_a == True:
                self._stiring = 90
                print("a released")
                self._flag_a = False

        if keys[K_RIGHT] or keys[K_d]:  # sends data through pipe while d or right is pressed
            self._stiring = max(0, self._stiring - 1)
            self._flag_d = True
            print("d")

        else:  # sends data once thorugh pipe if s or down is released
            if self._flag_d == True:
                self._stiring = 90
                print("d released")
                self._flag_d = False

        self._control.steer = (self._stiring-90)/120
        vehicle.apply_control(self._control)


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
    cam = camera(world)
    cam.attaching_camera()
    #control = carla.VehicleControl()
    #pipe = init_pipe_server()

    controller = keyboard(world)


#------------------------------------------------main loop -----------------------------------------------------------
    while spielaktiv:
        clock.tick_busy_loop(60) #fps controll
        if controller.parse_events(): #get keyboard events
            spielaktiv = False
        pygame.display.flip()


finally:
    print("destroying actors")
    for actor in actor_list:
        actor.destroy()