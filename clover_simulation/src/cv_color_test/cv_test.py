import cv2
import numpy as np

def getContours(binary_image):      
    _, contours, hierarchy = cv2.findContours(binary_image, 
                                              cv2.RETR_CCOMP, 
                                               cv2.CHAIN_APPROX_SIMPLE)
    return contours

def draw_contours(image, contours, image_name):
    index = -1 #means all contours
    thickness = 2 #thinkess of the contour line
    color = (255, 0, 255) #color of the contour line
    cv2.drawContours(image, contours, index, color, thickness)
    #cv2.imshow(image_name,image)

def contour_counter(mask):
    blur =  cv2.blur(mask,(5,5))
    contours = getContours(blur)
    counter = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        if area > 100:
            counter+=1
        print ("Chosen contour area: {}, Perimeter: {}".format(area, perimeter))
    return counter

def count_cargo(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    redLower = np.array((0, 42, 122), np.uint8) 
    redUpper = np.array((14, 141, 209), np.uint8) 

    greenLower = (52, 73, 118)
    greenUpper = (70, 162, 160)

    yellowLower = (29, 110, 112)
    yellowUpper = (37, 199, 225)

    blueLower = (90, 84, 80)
    blueUpper = (103, 225, 163)

    rgyb_counts = []

    red_mask = cv2.inRange(hsv, redLower, redUpper)
    rgyb_counts.append(contour_counter(red_mask))

    green_mask = cv2.inRange(hsv, greenLower, greenUpper)
    rgyb_counts.append(contour_counter(green_mask))

    yellow_mask = cv2.inRange(hsv, yellowLower, yellowUpper)
    rgyb_counts.append(contour_counter(yellow_mask))

    blue_mask = cv2.inRange(hsv, blueLower, blueUpper)
    rgyb_counts.append(contour_counter(blue_mask))
    print('Total: {0}'.format(sum(rgyb_counts)))
    print('rgyb: {0}'.format(rgyb_counts))
    


if __name__ == '__main__':
    image = cv2.imread('cv_color_test/5.jpg') #4.jpg     3.png
    count_cargo(image)
    #cv2.imshow("mask image r", red_mask)
    #cv2.imshow("mask image g", green_mask)
    #cv2.imshow("mask image y", yellow_mask)
    #cv2.imshow("mask image b", blue_mask)

    #cv2.waitKey(0)