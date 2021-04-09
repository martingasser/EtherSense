import numpy as np
import cv2
import queue
from threading import Thread


class Analysis:

    name = 'Surface'

    def __init__(self, process_async=False):
        self.process_async = process_async
        self.__bypass = False

        if self.process_async:
            self.frame_queue = queue.Queue()
            self.result_queue = queue.Queue()
            self.last_frame = None
            self.frames_dropped = 0

            self.run = True
            self.processing_thread = Thread(target=self.processing_thread)
            self.processing_thread.start()

    
    def __call__(self, frame):

        if self.__bypass:
            return None

        if self.process_async:
            self.frame_queue.put_nowait(frame)

            try:
                res = self.result_queue.get_nowait()
                self.last_frame = res
            except:
                self.frames_dropped += 1
                res = self.last_frame
            
            if res:
                res[1]['frames_dropped'] = self.frames_dropped
        else:            
            res = self.process(frame)
        
        return res

    def stop(self):
        if self.process_async:
            self.run = False
            self.processing_thread.join()

    @property
    def bypass(self):
        return self.__bypass

    @bypass.setter
    def bypass(self, b):
        self.__bypass = b

    def process(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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

    def processing_thread(self):
        while self.run:
            try:
                frame = self.frame_queue.get_nowait()
                self.frame_queue.queue.clear()
                res = self.process(frame)
                self.result_queue.put_nowait(res)
            except queue.Empty:
                pass
