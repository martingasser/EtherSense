#!/usr/bin/python
import sys, getopt
import signal
import asyncore
import numpy as np
import pickle
import socket
import struct
import cv2
import argparse
import importlib
from plugins import import_plugins
import time
import zmq

parser = argparse.ArgumentParser(description='Ethersense client.')
parser.add_argument('--plugins', metavar='N', type=str, nargs='+',
                    help='a list of plugins')
parser.add_argument('--gui', action='store_true')

args = parser.parse_args()

mc_ip_address = '224.0.0.1'

port = 1024
chunk_size = 4096

def main():
    client = EtherSenseClient()
    asyncore.loop()


class ZmqDispatcher(asyncore.dispatcher):

    def __init__(self, socket, map=None, *args, **kwargs):
        asyncore.dispatcher.__init__(self, None, map)
        self.set_socket(socket)
       
    def set_socket(self, sock, map=None):
        self.socket = sock
        self._fileno = sock.getsockopt(zmq.FD)
        self.add_channel(map)
    
    def bind(self, *args):
        self.socket.bind(self, *args)
    
    def connect(self, *args):
        self.socket.connect(*args)
        self.connected = True

    def writable(self):
        return False
        
    def send(self, data, *args):
        self.socket.send(data, *args)
    
    def recv(self, *args):
        return self.socket.recv(*args)

    def close(self):
        self.socket.close()
        super().close()

    def handle_read_event(self):
        # check if really readable
        revents = self.socket.getsockopt(zmq.EVENTS)
        while revents & zmq.POLLIN:
            self.handle_read()
            if self.socket.closed:
                break
            revents = self.socket.getsockopt(zmq.EVENTS)


class ImageClient(ZmqDispatcher):
    def __init__(self, socket, ethersense_client):
        ZmqDispatcher.__init__(self, socket)

        self.ethersense_client = ethersense_client
        self.plugins = []
        if args.plugins:
            self.plugins = import_plugins(args.plugins)
        
        self.buffer = bytearray()
       
    def handle_read(self):
        topic, data = self.socket.recv_multipart()
        self.buffer = data

        if topic == b'TIME':
            self.process_data()
            self.timestamp = struct.unpack('<d', self.buffer[0:8])[0]
        elif topic == b'RGB':
            self.color_array = pickle.loads(self.buffer)
        elif topic == b'DEPTH':
            self.depth_array = pickle.loads(self.buffer)
        elif topic == b'POSE':
            #self.pose_array = pickle.loads(self.buffer)
            #self.pose_array = struct.unpack('<18d', self.buffer)
            #self.pose_array = pickle.loads(self.buffer)
            self.pose_array = struct.unpack('<19d', self.buffer)
        else:
            plugin_id = topic
            if plugin_id in self.plugins:
                plugin_features_name = f'{plugin_id.decode()}_features'
                deserialized_features = self.plugins[plugin_id].deserialize_features(self.buffer)
                setattr(self, plugin_features_name, deserialized_features)

    def process_data(self):

        if hasattr(self, 'pose_array'):
            translation = self.pose_array[0:3]
            rotation = self.pose_array[3:7]
            velocity = self.pose_array[7:10]
            acceleration = self.pose_array[10:13]
            angular_velocity = self.pose_array[13:16]
            angular_acceleration = self.pose_array[16:19]
        
            translation_text = f'Translation: {translation[0]: 0.2f}, {translation[1]: 0.2f}, {translation[2]: 0.2f}'
            rotation_text = f'Rotation: {rotation[0]: 0.2f}, {rotation[1]: 0.2f}, {rotation[2]: 0.2f}'

            if hasattr(self, 'color_array'):
                cv2.putText(self.color_array, translation_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (65536), 2, cv2.LINE_AA)
                cv2.putText(self.color_array, rotation_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (65536), 2, cv2.LINE_AA)
            
        if hasattr(self, 'yolo_features'):
            plugin_features = getattr(self, 'yolo_features')
            color = (255, 0, 0)
            
            classes = []
            if hasattr(self, 'color_array'):
                for (classname, score, box) in zip(plugin_features['classes'], plugin_features['scores'], plugin_features['boxes']):
                    label = "%s : %f" % (classname, score)
                    cv2.rectangle(self.color_array, box, color, 2)
                    cv2.putText(self.color_array, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        if hasattr(self, 'color_array'):
            if args.gui:
                cv2.imshow("window", self.color_array)
        
        if args.gui:
            key = cv2.waitKey(1)
            if key == 27:
                self.close()
                self.ethersense_client.close()
    
    def readable(self):
        return True


class EtherSenseClient(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)

        self.connected = False
        self.server_address = ('', 1025)

        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.bind(self.server_address)

        self.ping_sent = False
        self.socket.settimeout(0)
        ttl = struct.pack('@i', 1)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        
    def writable(self): 
        return not self.ping_sent

    def readable(self):
        return not self.connected
        
    def handle_read(self):
        pair = self.socket.recvfrom(1024)
        
        if pair is not None:
            message, addr = pair
            print(f'Received {message.decode()} from {repr(addr)}')
            print ('Connecting to EtherSense server at %s' % repr(addr))
            
            ctx = zmq.Context()
            zmq_socket = ctx.socket(zmq.SUB)
            zmq_socket.connect(f'tcp://{addr[0]}:{addr[1]}')
            
            zmq_socket.subscribe(b'TIME')
            zmq_socket.subscribe(b'RGB')
            zmq_socket.subscribe(b'DEPTH')
            zmq_socket.subscribe(b'POSE')
            zmq_socket.subscribe(b'yolo')

            self.connected = True
            handler = ImageClient(zmq_socket, self)
        
    def handle_close(self):
        self.connected = False
    
    def handle_write(self):
        self.socket.sendto(b'ping', (mc_ip_address, port))
        self.ping_sent = True

def signal_handler(sig, frame):    
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    main()
