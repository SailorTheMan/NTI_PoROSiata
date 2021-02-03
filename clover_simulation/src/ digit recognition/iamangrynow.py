import numpy as np
import cv2

def compute_weight(file_path, photo, orb):
    
    img1 = cv2.imread(file_path,0)          # queryImage
    #img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = photo
    #img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
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
    return weight

def recognize(photo):
    # Initiate SIFT detector
    orb = cv2.ORB_create()
    weights = {}
    weights[0] = compute_weight(' digit recognition/cut_zero.png', photo, orb)
    weights[1] = compute_weight(' digit recognition/cut_one.png', photo, orb)
    weights[2] = compute_weight(' digit recognition/cut_two.png', photo, orb)
    weights[3] = compute_weight(' digit recognition/cut_three.png', photo, orb)
    print(min(weights, key=weights.get))

if __name__ == '__main__':
    img = cv2.imread(' digit recognition/rect_zero.png',0)   
    
    recognize(img)