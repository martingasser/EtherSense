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

from pythonosc import udp_client

parser = argparse.ArgumentParser(description='Ethersense client.')
parser.add_argument('--plugins', metavar='N', type=str, nargs='+',
                    help='a list of plugins')
parser.add_argument('--process_async', action='store_true')

parser.add_argument('--osc_ip', default='127.0.0.1')
parser.add_argument('--osc_port', type=int, default=8888)

args = parser.parse_args()

osc_client = udp_client.SimpleUDPClient(args.osc_ip, args.osc_port)

mc_ip_address = '224.0.0.1'

port = 1024
chunk_size = 4096

def main():
    multi_cast_message(mc_ip_address, port, 'EtherSensePing')
    # defer waiting for a response using Asyncore
    client = EtherSenseClient()
    asyncore.loop()

# client for each camera server 
class ImageClient(asyncore.dispatcher):
    def __init__(self, server, source, parent_client):
        asyncore.dispatcher.__init__(self, server)
        self.parent_client = parent_client

        self.run_surface = True
        self.run_yolo = True

        self.address = server.getsockname()[0]
        self.port = source[1]
        self.plugins = None
        if args.plugins:
            self.plugins = import_plugins(args.plugins)
        
        self.buffer = bytearray()
        self.windowName = self.port
        # open cv window which is unique to the port
        cv2.namedWindow("window"+str(self.windowName))
        self.remainingBytes = 0
        self.frame_id = 0
       
    def handle_read(self):
        if self.remainingBytes == 0:
            # get the expected frame size
            self.frame_length = struct.unpack('<I', self.recv(4))[0]
            self.remainingBytes = self.frame_length
        
        # request the frame data until the frame is completely in buffer
        if self.remainingBytes > 0:
            data = self.recv(self.remainingBytes)
            self.buffer += data
            self.remainingBytes -= len(data)
        
        # once the frame is fully recieved, process/display it
        if len(self.buffer) == self.frame_length:
            self.handle_frames()

    def handle_frames(self):
        # convert the frame from string to numerical data
        
        timestamp = struct.unpack('<d', self.buffer[0:8])[0]
        color_length = struct.unpack('<I', self.buffer[8:12])[0]
        depth_length = struct.unpack('<I', self.buffer[12:16])[0]
        pose_length = struct.unpack('<I', self.buffer[16:20])[0]
        # get the timestamp of the current frame

        color_start = 20
        color_end = color_start+color_length
        color_array = pickle.loads(self.buffer[color_start:color_end])

        depth_start = color_end
        depth_end = depth_start + depth_length
        depth_array = pickle.loads(self.buffer[depth_start:depth_end])

        pose_start = depth_end
        pose_end = pose_start + pose_length
        pose_array = pickle.loads(self.buffer[pose_start:pose_end])


        plugin_data_start = pose_end
        
        yolo_features = None

        while plugin_data_start < len(self.buffer):
            plugin_frame_length = struct.unpack('<I', self.buffer[plugin_data_start:plugin_data_start+4])[0]
            plugin_id = bytes(self.buffer[plugin_data_start+4:plugin_data_start+8])

            if plugin_id in self.plugins:
                deserialized_features = self.plugins[plugin_id].deserialize_features(self.buffer[plugin_data_start+4:plugin_data_start+4+plugin_frame_length])
                if plugin_id == b'yolo':
                    yolo_features = deserialized_features
                elif plugin_id == b'surf':
                    #print(deserialized_features)
                    pass
            plugin_data_start += plugin_frame_length+4

        translation = pose_array[0:3]
        rotation = pose_array[3:6]
        
        translation_text = f'Translation: {translation[0]: 0.2f}, {translation[1]: 0.2f}, {translation[2]: 0.2f}'
        rotation_text = f'Rotation: {rotation[0]: 0.2f}, {rotation[1]: 0.2f}, {rotation[2]: 0.2f}'

        cv2.putText(color_array, translation_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (65536), 2, cv2.LINE_AA)
        cv2.putText(color_array, rotation_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (65536), 2, cv2.LINE_AA)
        

        if yolo_features:
            color = (255, 0, 0)
            
            classes = []
            for (classname, score, box) in zip(yolo_features['classes'], yolo_features['scores'], yolo_features['boxes']):
                label = "%s : %f" % (classname, score)
                cv2.rectangle(color_array, box, color, 2)
                cv2.putText(color_array, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
        cv2.imshow("window"+str(self.windowName), color_array)

        osc_client.send_message('/translation', [translation[0], translation[1], translation[2]])
        osc_client.send_message('/rotation', [rotation[0], rotation[1], rotation[2]])

        key = cv2.waitKey(1)
        if key == 27:
            self.close()
            self.parent_client.close()
            
            
        # elif key == ord('s'):
        #     self.run_surface = not self.run_surface
        #     self.plugins['plugins.surface'].bypass = self.run_surface
        # elif key == ord('y'):
        #     self.run_yolo = not self.run_yolo
        #     self.plugins['plugins.yolo'].bypass = self.run_yolo
    
        self.buffer = bytearray()
        self.frame_id += 1
    
    def readable(self):
        return True

    
class EtherSenseClient(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.plugin = None
        self.server_address = ('', 1024)
        # create a socket for TCP connection between the client and server
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        
        self.bind(self.server_address) 	
        self.listen(10)

    def writable(self): 
        return False

    def readable(self):
        return True
        
    def handle_connect(self):
        print("connection recieved")

    def handle_accept(self):
        pair = self.accept()
        
        if pair is not None:
            sock, addr = pair
            print ('Incoming connection from %s' % repr(addr))
            # when a connection is attempted, delegate image receival to the ImageClient 
            handler = ImageClient(sock, addr, self)

def multi_cast_message(ip_address, port, message):
    multicast_group = (ip_address, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send data to the multicast group
        print('sending "%s"' % message + str(multicast_group))
        sent = sock.sendto(message.encode(), multicast_group)
    except socket.timeout:
        print('timed out, no more responses')
    finally:
        print(sys.stderr, 'closing socket')
        sock.close()

def signal_handler(sig, frame):    
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    main()
