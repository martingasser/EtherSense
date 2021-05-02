import numpy as np
import cv2
import queue
from threading import Thread, Barrier
import pickle
import struct
from .plugin import EtherSensePlugin

class Plugin(EtherSensePlugin):

    name = 'Weed Detector'
    plugin_id = b'weed'

    def __init__(self, process_async=False, barrier=None):
        super().__init__(process_async, barrier)

    def process(self, frame):
        blurred = cv2.GaussianBlur(frame, (25,25), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        hsv_min = (30, 20, 20)
        hsv_max = (90, 255, 255)
        mask = cv2.inRange(hsv, np.array(hsv_min), np.array(hsv_max))
        masked = cv2.bitwise_and(hsv, hsv, mask=mask)

        morph_kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (6,6))
            
        morphed = cv2.morphologyEx(masked, cv2.MORPH_CLOSE, morph_kernel, 4)
        morphed = cv2.dilate(morphed, morph_kernel, iterations=1)
        bgr = cv2.cvtColor(morphed, cv2.COLOR_HSV2BGR)
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(
            gray,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(frame, contours, -1, (0,255,0), 3)

        area = 0
        for cnt in contours:
            area += cv2.contourArea(cnt)

        amount = area / (frame.shape[0]*frame.shape[1])
        
        features = {
            'weed_percentage': amount
        }

        return (frame, features)

    @staticmethod
    def serialize_features(features):
        id_ser = Plugin.plugin_id
        weed_percentage_ser = struct.pack('<f', features['weed_percentage'])
        return b''.join([id_ser, weed_percentage_ser])

    
    @staticmethod
    def deserialize_features(data):
        id_deser = data[0:4]
        weed_percentage_deser = struct.unpack('<f', data[4:8])[0]
        features = {
            'weed_percentage': weed_percentage_deser
        }
        return features
