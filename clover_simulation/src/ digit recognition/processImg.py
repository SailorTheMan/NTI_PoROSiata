import numpy as np
import cv2
import time


def read_rgb_image(image_name, show):
    rgb_image = cv2.imread(image_name)
    if show: 
        cv2.imshow("RGB Image",rgb_image)
    return rgb_image

def convert_rgb_to_gray(rgb_image,show):
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    if show: 
        cv2.imshow("Gray Image",gray_image)
    return gray_image

def convert_gray_to_binary(gray_image, adaptive, show):
    if adaptive: 
        binary_image = cv2.adaptiveThreshold(gray_image, 
                            255, 
                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                            cv2.THRESH_BINARY_INV, 151, 2)
    else:
        _,binary_image = cv2.threshold(gray_image,200,255,cv2.THRESH_BINARY_INV)
    if show:
        cv2.imshow("Binary Image", binary_image)
    return binary_image    

def getContours(binary_image):      
    _, contours, hierarchy = cv2.findContours(binary_image, 
                                              cv2.RETR_CCOMP, 
                                               cv2.CHAIN_APPROX_SIMPLE)
    return contours

def recognise_number(image, model):

    ############################# testing part  #########################

    im = image
    out = np.zeros(im.shape,np.uint8)
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)

    _,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        cnt_area = cv2.contourArea(cnt)
        if cnt_area>200 and cnt_area < 900:     #values to distinguish digits inside
            [x,y,w,h] = cv2.boundingRect(cnt)
            if  h>28:
                cv2.rectangle(out,(x,y),(x+w,y+h),(0,255,0),2)
                roi = thresh[y:y+h,x:x+w]
                roismall = cv2.resize(roi,(10,10))
                roismall = roismall.reshape((1,100))
                roismall = np.float32(roismall)
                retval, results, neigh_resp, dists = model.findNearest(roismall, k = 1) 
                string = str(int((results[0][0])))
                cv2.putText(im,string,(x,y+h),0,2,(10,127,207), 2)
                print(string)

    cv2.imshow('im',im)
    cv2.imshow('out',out)
    cv2.waitKey(0)


def draw_contours(image, contours, image_name):
    index = -1 #means all contours
    thickness = 2 #thinkess of the contour line
    color = (255, 0, 255) #color of the contour line
    cv2.drawContours(image, contours, index, color, thickness)
    cv2.imshow(image_name,image)

def get_contour_center(contour):
    M = cv2.moments(contour)
    cx=-1
    cy=-1
    if (M['m00']!=0):
        cx= int(M['m10']/M['m00'])
        cy= int(M['m01']/M['m00'])
    return cx, cy

def process_contours(binary_image, rgb_image, contours, model):
    black_image = np.zeros([binary_image.shape[0], binary_image.shape[1],3],'uint8')
    out = np.zeros_like(rgb_image) # Extract out the object and place into output image
    idx = 0
    for c in contours:
        area = cv2.contourArea(c)
        perimeter= cv2.arcLength(c, True)

        if (area > 3000 and perimeter < 1000):              # values to distinguish our countours
            print ("Chosen contour area: {}, Perimeter: {}".format(area, perimeter))
            cv2.drawContours(rgb_image, [c], -1, (150,250,150), 1)
            cv2.drawContours(black_image, [c], -1, (150,250,150), 1)

            #leftmost = tuple(c[c[:,:,0].argmin()][0])
            #rightmost = tuple(c[c[:,:,0].argmax()][0])
            #topmost = tuple(c[c[:,:,1].argmin()][0])
            #bottommost = tuple(c[c[:,:,1].argmax()][0])
            
            mask = np.zeros_like(rgb_image) # Create mask where white is what we want, black otherwise
            cv2.drawContours(mask, contours, idx, 255, -1) # Draw filled contour in mask
            
            out[mask == 255] = rgb_image[mask == 255]

            #rgb_image = cv2.line(rgb_image,leftmost,rightmost,(255,0,0),3)
            #rgb_image = cv2.line(rgb_image,topmost,bottommost,(255,0,0),3)

            recognise_number(out, model)

            
        idx+=1
        print ("Area: {}, Perimeter: {}".format(area, perimeter))

    print ("number of contours: {}".format(len(contours)))
    cv2.imshow("RGB Image Contours",rgb_image)
    cv2.imshow("Black Image Contours",black_image)

if __name__ == '__main__':
    image_name = "three_2.png"
    rgb_image = read_rgb_image(image_name, True)
    gray_image= convert_rgb_to_gray(rgb_image,True)
    binary_image = convert_gray_to_binary(gray_image, True, True)

    #######   training part    ############### 
    samples = np.loadtxt('generalsamples.data',np.float32)
    responses = np.loadtxt('generalresponses.data',np.float32)
    responses = responses.reshape((responses.size,1))

    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)
    print(model)
    print('Training done')

    contours = getContours(binary_image)
    #draw_contours(rgb_image, contours,"RGB Contours")
    process_contours(binary_image, rgb_image, contours, model)
    
    cv2.waitKey(0)
    time.sleep(10)
    print('AAAAAAAAAAAAAAAAAAAAAAA')
    cv2.destroyAllWindows()