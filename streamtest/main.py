import numpy as np
import cv2
import zmq
import pickle

zmq_ctx = zmq.Context()
zmq_socket = zmq_ctx.socket(zmq.PUB)
zmq_socket.bind("tcp://*:1024")

cap = cv2.VideoCapture('sample.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret:
        cv2.imshow('frame', frame)
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    color_data = pickle.dumps(frame)
    zmq_socket.send_multipart([b'RGB', color_data])

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()