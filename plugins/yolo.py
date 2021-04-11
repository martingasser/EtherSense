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


    @staticmethod
    def serialize_features(features):
        id_ser = Plugin.plugin_id
        classes_ser = pickle.dumps(features['classes'])
        scores_ser = pickle.dumps(features['scores'])
        bytes_classes_ser = struct.pack('<I', len(classes_ser))
        bytes_scores_ser = struct.pack('<I', len(classes_ser))
        return b''.join([id_ser, bytes_classes_ser, classes_ser, bytes_scores_ser, scores_ser])

    
    @staticmethod
    def deserialize_features(data):
        id_deser = data[0:4]
        bytes_classes_deser = struct.unpack('<I', data[4:8])[0]
        classes_deser = pickle.loads(data[8:8+bytes_classes_deser])
        bytes_scores_deser = struct.unpack('<I', data[8+bytes_classes_deser:8+bytes_classes_deser+4])[0]
        scores_deser = pickle.loads(data[8+bytes_scores_deser+4:8+bytes_scores_deser+4+bytes_scores_deser])
        
        features = {
            'classes': classes_deser,
            'scores': scores_deser
        }
        return features
