import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv_test


def image_callback(data):
    img = bridge.imgmsg_to_cv2(data, 'bgr8')  # OpenCV image

    cv_test.count_cargo(img)

    #imgStack = stackImages(1.0, ([img, imgGray, imgCanny], 
    #                             [imgDil, imgContour, imgCenters]))

    #image_pub.publish(bridge.cv2_to_imgmsg(imgStack, 'bgr8'))

rospy.init_node('computer_vision_sample')
image_pub = rospy.Publisher('~debug', Image, queue_size=1)
maxRect_pub = rospy.Publisher('maxRect', String, queue_size=1)
bridge = CvBridge()

image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback)

rospy.spin()