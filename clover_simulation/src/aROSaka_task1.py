# Information: https://clover.coex.tech/en/snippets.html#navigate_wait

import math
import rospy
from clover import srv
from pyzbar import pyzbar
from cv_bridge import CvBridge
from std_srvs.srv import Trigger
from sensor_msgs.msg import Image

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

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


bridge = CvBridge()

# Image subscriber callback function
def get_target_from_barcode(barcodes):
        for barcode in barcodes:
            b_data = barcode.data.encode("utf-8")
            b_type = barcode.type
            (x, y, w, h) = barcode.rect
            xc = x + w/2
            yc = y + h/2
            print ("Found QR CODE with data {}".format(b_data))
            map_x, map_y = b_data.split(' ')
            return map_x, map_y


# Take off 1 meter
navigate_wait(z=1, speed=1.0, frame_id='body', auto_arm=True)
print('lifted off')
navigate_wait(x=2, z=1, speed=1.0, frame_id='aruco_map', auto_arm=False)
print('target approached')

for i in range(3):

    while True:
        img = bridge.imgmsg_to_cv2(rospy.wait_for_message('main_camera/image_raw', Image), 'bgr8')
        barcodes = pyzbar.decode(img)
        if len(barcodes) == 0: 
            print('searching for QR codes...')
            continue
        break

    map_x, map_y = get_target_from_barcode(barcodes)

    navigate_wait(x=float(map_x), y=float(map_y), z=1, speed=1.0, frame_id='aruco_map', auto_arm=True)
    print('target approached')
    rospy.sleep(1)


# Fly forward 1 m
# navigate_wait(x=5, y=0, frame_id='aruco_map')


rospy.sleep(0.5)
print('landing')
# Land
land()

print('drone has landed')
