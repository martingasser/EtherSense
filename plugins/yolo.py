import cv2
import pathlib
import queue
from threading import Thread

CONFIDENCE_THRESHOLD = 0.2
NMS_THRESHOLD = 0.4

class Analysis:

    name = 'YOLO object detection'

    def __init__(self, process_async=True):
        self.__bypass = False

        try:
            path = pathlib.Path(__file__).parent.absolute()

            self.class_names = []
            with open(str(path / 'classes.txt'), 'r') as f:
                self.class_names = [cname.strip() for cname in f.readlines()]

            self.net = cv2.dnn.readNet(str(path / 'yolov4-tiny.weights'), str(path / 'yolov4-tiny.cfg'))
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

            self.model = cv2.dnn_DetectionModel(self.net)
            self.model.setInputParams(size=(320, 320), scale=1/255, swapRB=True)

            self.process_async = process_async

            if self.process_async:
                self.frame_queue = queue.Queue()
                self.result_queue = queue.Queue()
                self.last_frame = None
                self.frames_dropped = 0

                self.run = True
                self.processing_thread = Thread(target=self.processing_thread)
                self.processing_thread.start()
        except Exception as ex:
            print(ex)
        

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
        class_ids, scores, boxes = self.model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        color = (255, 0, 0)
        
        classes = []
        for (classid, score, box) in zip(class_ids, scores, boxes):
            class_name = self.class_names[classid[0]]
            label = "%s : %f" % (class_name, score)
            cv2.rectangle(frame, box, color, 2)
            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            classes.append(class_name)


        features = {
            'classes': classes,
            'scores': scores
        }
        return (frame, features)

    def processing_thread(self):
        while self.run:
            try:
                frame = self.frame_queue.get_nowait()
                self.frame_queue.queue.clear()
                res = self.process(frame)
                self.result_queue.put_nowait(res)
            except queue.Empty:
                pass
            

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
