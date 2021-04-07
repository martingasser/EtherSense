#!/usr/bin/python
import sys, getopt
import asyncore
import numpy as np
import pickle
import socket
import struct
import cv2
import json

import importlib

mc_ip_address = '224.0.0.1'

port = 1024
chunk_size = 4096

def main(plugin):
    multi_cast_message(mc_ip_address, port, 'EtherSensePing')
    # defer waiting for a response using Asyncore
    client = EtherSenseClient(plugin)
    asyncore.loop()

# client for each camera server 
class ImageClient(asyncore.dispatcher):
    def __init__(self, server, source, plugin):   
        asyncore.dispatcher.__init__(self, server)
        self.address = server.getsockname()[0]
        self.port = source[1]
        if plugin:
            try:
                self.plugin = importlib.import_module(plugin)
            except:
                print('could not load plugin')
        else:
            self.plugin = None
        
        self.buffer = bytearray()
        self.windowName = self.port
        # open cv window which is unique to the port 
        cv2.namedWindow("window"+str(self.windowName))
        self.remainingBytes = 0
        self.frame_id = 0
       
    def handle_read(self):
        if self.remainingBytes == 0:
            # get the expected frame size
            self.color_length = struct.unpack('<I', self.recv(4))[0]
            self.depth_length = struct.unpack('<I', self.recv(4))[0]
            self.pose_length = struct.unpack('<I', self.recv(4))[0]
            # get the timestamp of the current frame
            self.timestamp = struct.unpack('<d', self.recv(8))
            self.frame_length = self.color_length + self.depth_length + self.pose_length
            self.remainingBytes = self.frame_length
        
        # request the frame data until the frame is completely in buffer
        data = self.recv(self.remainingBytes)
        self.buffer += data
        self.remainingBytes -= len(data)
        # once the frame is fully recieved, process/display it
        if len(self.buffer) == self.frame_length:
            self.handle_frames()

    def handle_frames(self):
        # convert the frame from string to numerical data
        color_array = pickle.loads(self.buffer[0:self.color_length])

        depth_end = self.color_length+self.depth_length
        depth_array = pickle.loads(self.buffer[self.color_length:depth_end])

        pose_start = self.color_length+self.depth_length
        pose_end = pose_start + self.pose_length
        pose_array = pickle.loads(self.buffer[pose_start:pose_end])

        translation = pose_array[0:3]
        rotation = pose_array[3:6]
        
        if self.plugin:
            results = self.plugin.process(color_array)
            cv2.imshow("window"+str(self.windowName), results[0])
            features = results[1]
            # TODO: what to do with the features? output plugin? send via osc?
            #print(features['num_keypoints'])
        else:
            translation_text = f'Translation: {translation[0]: 0.2f}, {translation[1]: 0.2f}, {translation[2]: 0.2f}'
            rotation_text = f'Rotation: {rotation[0]: 0.2f}, {rotation[1]: 0.2f}, {rotation[2]: 0.2f}'
            big_color = cv2.resize(color_array, (0,0), fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
            cv2.putText(big_color, translation_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (65536), 2, cv2.LINE_AA)
            cv2.putText(big_color, rotation_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (65536), 2, cv2.LINE_AA)
            cv2.imshow("window"+str(self.windowName), big_color)

        if cv2.waitKey(1) == 27:
            exit()
        self.buffer = bytearray()
        self.frame_id += 1
    
    def readable(self):
        return True

    
class EtherSenseClient(asyncore.dispatcher):
    def __init__(self, plugin):
        asyncore.dispatcher.__init__(self)
        self.plugin = plugin
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
            handler = ImageClient(sock, addr, self.plugin)

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

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main(None)
