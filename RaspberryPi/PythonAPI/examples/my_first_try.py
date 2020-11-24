import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
    print(sys.version_info.major)
    print(sys.version_info.minor)
except IndexError:
    pass

import carla
import random
import time
import numpy as np
import cv2
import pygame

pygame.init()

#--------------------------beginnning
# constants
IM_WIDTH = 640
IM_HEIGHT = 480


def process_img(image):
    i = np.array(image.raw_data)  # convert to an array
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]
    cv2.imshow("",i3)
    cv2.waitKey(1)
    return i3 / 255.0


# list with all the actors
actor_list = []
try:
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
    # applying speed
    #vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
    # add the spawend vehicle to the actors list
    actor_list.append(vehicle)


# ---------------------------------------attaching a camera----------

    bp_cam = blueprint_library.find('sensor.camera.rgb')
    # changing image dimesnions
    bp_cam.set_attribute('image_size_x', f'{IM_WIDTH}')
    bp_cam.set_attribute('image_size_y', f'{IM_HEIGHT}')
    bp_cam.set_attribute('fov', '110')
    # adding the camera to the car
    spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    sensor = world.spawn_actor(bp_cam, spawn_point, attach_to=vehicle)
    # add to actors list
    actor_list.append(sensor)

    # get the camera data
    sensor.listen(lambda data: process_img(data))
    time.sleep(10)

'''
# -------------------manual_control-----------------------------
    QUIT = True
    while QUIT:
        print("inloop")
        for event in pygame.event.get():
            print("in")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steering=0.0))

                elif event.key == pygame.K_s:
                    vehicle.apply_control(carla.VehicleControl(throttle=-1.0, steering=0.0))

                elif event.key == pygame.K_a:
                    vehicle.apply_control(carla.VehicleControl(throttle=0.0, steering=-30.0))

                elif event.key == pygame.K_d:
                    vehicle.apply_control(carla.VehicleControl(throttle=0.0, steering=30.0))

                elif event.key == pygame.K_f:
                    QUIT = False
                    print("f pressed")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    vehicle.apply_control(carla.VehicleControl(throttle=0.0, steering=0.0))

                elif event.key == pygame.K_s:
                    vehicle.apply_control(carla.VehicleControl(throttle=0.0, steering=0.0))

                elif event.key == pygame.K_a:
                    vehicle.apply_control(carla.VehicleControl(throttle=0.0, steering=0.0))

                elif event.key == pygame.K_d:
                    vehicle.apply_control(carla.VehicleControl(throttle=0.0, steering=0.0))
'''
finally:
    print("destroying actors")
    for actor in actor_list:
        actor.destroy()
    print("destroyed")

