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


SAFE_HEIGHT = 2.0
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


def getcolor():
    
    img = bridge.imgmsg_to_cv2(rospy.wait_for_message('main_camera/image_raw', Image), 'bgr8')
    cv2.imshow('img', img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    col = 0
    for _ in range(10):
        (h, _, _) = img[120, 160]
        
        col += h
        # print(col)
        rospy.sleep(0.1)
    col = col / 10
    if (col < 5):
        return 'red'
    if (col > 25 and col < 35):
        return 'yellow'
    if (col > 55 and col < 65):
        return 'green'
     
    print('error color')
    return 'error'


rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

bridge = CvBridge()

# Take off to safe height 
navigate_wait(z=SAFE_HEIGHT, speed=1.0, frame_id='body', auto_arm=True)
print('lifted off')

coordinates = [[0, 2.5], [3.5, 0.5], [2, 1.5], [3.5, 3.5]]
file = open("report.txt", "w") 
file.write("Number  Coordinates   Color\n")

for i in range(4):

    map_x, map_y = coordinates[i]
    print(map_x, map_y)
    navigate_wait(x=float(map_x), y=float(map_y), z=0.5, speed=1.0, frame_id='aruco_map', auto_arm=True)
    print('target approached')

    color = getcolor()
    print("Coordinate: {}, {}; color: {}".format(map_x, map_y, color))

    file.write("  {}     x={}, y={}     {}\n".format(i+1, map_x, map_y, color))

    rospy.sleep(1)


navigate_wait(x=0, y = 0, z = 0.5, speed=1.0, frame_id='aruco_map', auto_arm=False)

print('target approached')

rospy.sleep(0.5)
 
print('landing')
# Land
land()
print('drone has landed')

file.close()
