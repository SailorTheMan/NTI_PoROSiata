# Information: https://clover.coex.tech/en/snippets.html#navigate_wait

import os
import math
import rospy
from clover import srv
from cv_bridge import CvBridge
from std_msgs.msg import String
from std_srvs.srv import Trigger
from clover.srv import SetLEDEffect


SAFE_HEIGHT = 2.5
SPEED = 0.3
CAM_HEIGHT = 280
CAM_WIDTH = 320
TOLERANCE = 30
KX = 0.001
KY = 0.001

RECT = [0, 0, 0, 0]


def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), yaw_rate=0, speed=SPEED, \
        frame_id='body', tolerance=0.01, auto_arm=False):

    res = navigate(x=x, y=y, z=z, yaw=yaw, yaw_rate=yaw_rate, speed=speed, \
        frame_id=frame_id, auto_arm=auto_arm)

    if not res.success:
        return res

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            return res
        rospy.sleep(0.2)


def rect_callback(data):
    print(str(data))
    # x, y, w, h = str(data).split(' ')
    # RECT[0] = x
    # RECT[1] = y
    # RECT[2] = w
    # RECT[3] = h

def center_the_rect():
    x_c = RECT[0] + RECT[2] / 2
    y_c = RECT[1] + RECT[3] / 2

    cam_x_c = CAM_WIDTH / 2
    cam_y_c = CAM_HEIGHT / 2

    while (abs(cam_x_c - x_c) > TOLERANCE) or (abs(cam_y_c - y_c) > TOLERANCE):
        d_x = cam_x_c - x_c
        d_y = cam_y_c - y_c

        navigate_wait(x= d_x * KX, y= d_y * KY, z= 0, frame_id='body', auto_arm=True)
    

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

rospy.Subscriber('maxRect', String, rect_callback)
rospy.spin()

# Take off to safe height 
# navigate_wait(z=0.9, frame_id='body', auto_arm=True)
print('control is mine')

# navigate_wait(x=0.1, z=0, frame_id='body', auto_arm=True)
print('messed up')

# center_the_rect()
print('centered')



