import numpy as np
import cv2

###          HOW TO USE          ###
# Call  recognize_digit([rgb_photo])
# Returned value is recognized digit

def compute_weight(file_path, photo, orb):
    
    img1 = cv2.imread(file_path,0)          # queryImage
    img1 = cv2.adaptiveThreshold(img1, 
                            255, 
                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                            cv2.THRESH_BINARY_INV, 151, 2)
    img2 = photo
    img2 = cv2.adaptiveThreshold(img2, 
                            255, 
                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                            cv2.THRESH_BINARY_INV, 151, 2)

    '''### SHAPE MATCHING TEST ####
    _, contours,hierarchy = cv2.findContours(img1,2,1)
    cnt1 = contours[3]
    _, contours,hierarchy = cv2.findContours(img2,2,1)
    cnt2 = contours[3]
    
    ret = cv2.matchShapes(cnt1,cnt2,1,0.0)
    print ret

    ### END SHAPE MATCHING TEST ###'''

    # find the keypoints and descriptors with SIFT
    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(img2,None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # Match descriptors.
    matches = bf.match(des1,des2)
    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)
    weight = 1000
    matches_sum = 0
    for match in matches:
        matches_sum += match.distance
    
    avg_dist = matches_sum / len(matches)
    weight = avg_dist
    

    if __name__ == '__main__':
        img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:10], None, flags=2)
        #cv2.drawContours(img3, contours, -1, (255, 0, 255), 2)
        print('File: {0}'.format(file_path))
        print('Median distance: {0}'.format(matches[len(matches)/2].distance))
        print('Average distance: {0}'.format(avg_dist))
        plt.imshow(img3),plt.show()

    return weight

def recognize_digit(photo):
    # Initiate SIFT detector
    orb = cv2.ORB_create()      #     TODO:     |
    weights = {}                #  FIX THIS     V
    weights[0] = compute_weight(' digit recognition/new_zero.png', photo, orb)
    weights[1] = compute_weight(' digit recognition/new_one.png', photo, orb)
    weights[2] = compute_weight(' digit recognition/new_two.png', photo, orb)
    weights[3] = compute_weight(' digit recognition/new_three.png', photo, orb)
    #print(weights.values())
    return(min(weights, key=weights.get))

if __name__ == '__main__':
    from matplotlib import pyplot as plt
    img = cv2.imread(' digit recognition/rect_2.png',0)   
    
    print recognize_digit(img)