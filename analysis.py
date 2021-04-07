import numpy as np
import cv2

def process(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray,(3,3))
    img_log = (np.log(blur+1)/(np.log(1+np.max(blur))))*255
    img_log = np.array(img_log,dtype=np.uint8)
    bilateral = cv2.bilateralFilter(img_log, 5, 75, 75)
    edges = cv2.Canny(bilateral,100,200)
    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    orb = cv2.ORB_create(nfeatures=1500)
    keypoints, descriptors = orb.detectAndCompute(closing, None)
    feature_img = cv2.drawKeypoints(closing, keypoints, None)
    features = {
        'keypoints': [k.pt for k in keypoints],
        'num_keypoints': len(keypoints)
    }
    return (feature_img, features)