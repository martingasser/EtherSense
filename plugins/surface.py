import numpy as np
import cv2
import queue
from threading import Thread, Barrier
import pickle
import struct
from .plugin import EtherSensePlugin

class Plugin(EtherSensePlugin):

    name = 'Surface'
    plugin_id = b'surf'

    def __init__(self, process_async=False, barrier=None):
        super().__init__(process_async, barrier)

    def process(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.blur(gray,(3,3))
        img_log = 255.0 * (np.log(blur+1.0) / (np.log(1.0 + np.max(blur))))
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

    @staticmethod
    def serialize_features(features):
        id_ser = Plugin.plugin_id
        keypoints_ser = pickle.dumps(features['keypoints'])
        num_keypoints_ser = struct.pack('<I', len(keypoints_ser))
        return b''.join([id_ser, num_keypoints_ser, keypoints_ser])

    
    @staticmethod
    def deserialize_features(data):
        id_deser = data[0:4]
        num_keypoints_deser = struct.unpack('<I', data[4:8])[0]
        keypoints_deser = pickle.loads(data[8:8 + num_keypoints_deser])
        features = {
            'keypoints': keypoints_deser,
            'num_keypoints': len(keypoints_deser)
        }
        return features
