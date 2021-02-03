import cv2
import numpy as np

img = cv2.imread('3.png') #4.jpg     3.png
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

redLower = np.array((0, 42, 122), np.uint8) 
redUpper = np.array((14, 141, 209), np.uint8) 

greenLower = (52, 73, 118)
greenUpper = (70, 162, 160)

yellowLower = (29, 110, 112)
yellowUpper = (37, 199, 225)

blueLower = (90, 84, 80)
blueUpper = (103, 225, 163)

red_mask = cv2.inRange(hsv, redLower, redUpper)
green_mask = cv2.inRange(hsv, greenLower, greenUpper)
yellow_mask = cv2.inRange(hsv, yellowLower, yellowUpper)
blue_mask = cv2.inRange(hsv, blueLower, blueUpper)


cv2.imshow("mask image r", red_mask)
cv2.imshow("mask image g", green_mask)
cv2.imshow("mask image y", yellow_mask)
cv2.imshow("mask image b", blue_mask)

cv2.waitKey(0)
