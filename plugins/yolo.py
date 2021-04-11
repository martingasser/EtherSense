import cv2
import pathlib
import queue
from threading import Thread, Barrier
from .plugin import EtherSensePlugin

CONFIDENCE_THRESHOLD = 0.2
NMS_THRESHOLD = 0.4

class Plugin(EtherSensePlugin):

    name = 'YOLO object detection'
    plugin_id = b'yolo'

    def __init__(self, process_async=True, barrier=None):
        super().__init__(process_async, barrier)

        path = pathlib.Path(__file__).parent.absolute()

        self.class_names = []
        with open(str(path / 'classes.txt'), 'r') as f:
            self.class_names = [cname.strip() for cname in f.readlines()]

        self.net = cv2.dnn.readNet(str(path / 'yolov4-tiny.weights'), str(path / 'yolov4-tiny.cfg'))
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        self.model = cv2.dnn_DetectionModel(self.net)
        self.model.setInputParams(size=(320, 320), scale=1/255, swapRB=True)        

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
