# Information: https://clover.coex.tech/en/snippets.html#navigate_wait

import os
import math
import rospy
import cv2
from clover import srv
from pyzbar import pyzbar
from cv_bridge import CvBridge
from std_srvs.srv import Trigger
from sensor_msgs.msg import Image
from clover.srv import SetLEDEffect
from mavros_msgs.srv import SetMode


SAFE_HEIGHT = 2.5
SPEED = 0.3
MARKER_DIST = 0.9
RED_BOUNDS = (0, 5)
YELLOW_BOUNDS = (25, 35)
BLUE_BOUNDS = (10, 15) #check bounds
GREEN_BOUNDS = (55, 65)


def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), yaw_rate=0, speed=0.5, \
        frame_id='body', tolerance=0.2, auto_arm=False):

    res = navigate(x=x, y=y, z=z, yaw=yaw, yaw_rate=yaw_rate, speed=speed, \
        frame_id=frame_id, auto_arm=auto_arm)

    if not res.success:
        return res

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            return res
        rospy.sleep(0.2)


def take_picture(title):
    rospy.sleep(1)
    img = bridge.imgmsg_to_cv2(rospy.wait_for_message('main_camera/image_raw', Image), 'bgr8')
    cv2.imwrite(title, img)

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)
set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)
set_mode = rospy.ServiceProxy('mavros/set_mode', SetMode)

bridge = CvBridge()

# Take off to safe height 
navigate_wait(z=SAFE_HEIGHT, speed=SPEED, frame_id='body', auto_arm=True)
print('lifted off')

for i in range(2, 4):
    navigate_wait(x=0.9, y=0.9, z=i, speed=SPEED, frame_id='aruco_map', auto_arm=False)

    for x in range(0, 4):
        for y in range(0, 6):
            navigate_wait(x=x*MARKER_DIST, y=y*MARKER_DIST, z=i, speed=SPEED, frame_id='aruco_map', auto_arm=False)
            rospy.sleep(1)
            take_picture('data/' + str(x) + '_' + str(y) + '_' + str(i) + '.png')
            print('target approached')