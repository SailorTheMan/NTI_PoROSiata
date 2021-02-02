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

bridge = CvBridge()

take_picture('1.png')


print('target approached')

rospy.sleep(0.5)
 
print('landing')
# Land
land()
print('drone has landed')

#file.close()
