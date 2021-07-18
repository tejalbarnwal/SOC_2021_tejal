import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
 

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
import time
import numpy as np
import cv2

IM_WIDTH = 640
IM_HEIGHT = 480

rospy.init_node("hi")
bridge = CvBridge()
pub = rospy.Publisher('image', Image, queue_size=10)


fourcc = cv2.VideoWriter_fourcc(*'XVID');   #or fourcc = cv2.VideoWriter_fourcc('X','V','I','D');
out = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480));  

def process_img(image):
    i = np.array(image.raw_data)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]

    imgMsg = bridge.cv2_to_imgmsg(i3, "bgr8")
    pub.publish(imgMsg)
    print("published----------------")
    cv2.imshow("", i3)
    out.write(i3)
    cv2.waitKey(1)
    return i3/255.0


actor_list = []
try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    world = client.get_world()

    blueprint_library = world.get_blueprint_library()

    bp = blueprint_library.filter('model3')[0]
    print(bp)

    spawn_point = random.choice(world.get_map().get_spawn_points())

    vehicle = world.spawn_actor(bp, spawn_point)
    # vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
    vehicle.set_autopilot(True)  # if you just wanted some NPCs to drive.

    actor_list.append(vehicle)

    # https://carla.readthedocs.io/en/latest/cameras_and_sensors
    # get the blueprint for this sensor
    blueprint = blueprint_library.find('sensor.camera.rgb')
    # change the dimensions of the image
    blueprint.set_attribute('image_size_x', str(IM_WIDTH))
    blueprint.set_attribute('image_size_y', str(IM_HEIGHT))
    blueprint.set_attribute('fov', '110')

    # Adjust sensor relative to vehicle
    spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))

    # spawn the sensor and attach to vehicle.
    sensor = world.spawn_actor(blueprint, spawn_point, attach_to=vehicle)

    # add sensor to list of actors
    actor_list.append(sensor)

    # do something with this sensor
    sensor.listen(lambda data: process_img(data))
    

    time.sleep(300)
    out.release()

finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')

