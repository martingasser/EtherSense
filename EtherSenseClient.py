#!/usr/bin/python
import sys, getopt
import asyncore
import numpy as np
import pickle
import socket
import struct
import cv2
import argparse
import importlib

parser = argparse.ArgumentParser(description='Ethersense client.')
parser.add_argument('--plugins', metavar='N', type=str, nargs='+',
                    help='a list of plugins')
parser.add_argument('--process_async', action='store_true')
args = parser.parse_args()

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
    def __init__(self, server, source):   
        asyncore.dispatcher.__init__(self, server)

        self.run_surface = True
        self.run_yolo = True

        self.address = server.getsockname()[0]
        self.port = source[1]
        self.plugins = {}
        if args.plugins:
            try:
                for plugin in args.plugins:
                    plugin_lib = importlib.import_module(plugin)
                    self.plugins[plugin] = plugin_lib.Analysis(process_async=args.process_async)
            except:
                print('could not load plugin')
        
        self.buffer = bytearray()
        self.windowName = self.port
        # open cv window which is unique to the port

        if len(self.plugins):
            for plugin_name in self.plugins:
                plugin = self.plugins[plugin_name]
                cv2.namedWindow(f'window {plugin.name}')
        else:
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
        
        if len(self.plugins):
            for plugin_name in self.plugins:
                plugin = self.plugins[plugin_name]
                results = plugin(color_array)
                if results:
                    cv2.imshow(f'window {plugin.name}', results[0])
                    features = results[1]
                    #print(features)
                    # TODO: what to do with the features? output plugin? send via osc?
                    #print(features['num_keypoints'])
        else:
            translation_text = f'Translation: {translation[0]: 0.2f}, {translation[1]: 0.2f}, {translation[2]: 0.2f}'
            rotation_text = f'Rotation: {rotation[0]: 0.2f}, {rotation[1]: 0.2f}, {rotation[2]: 0.2f}'
            big_color = cv2.resize(color_array, (0,0), fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
            cv2.putText(big_color, translation_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (65536), 2, cv2.LINE_AA)
            cv2.putText(big_color, rotation_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (65536), 2, cv2.LINE_AA)
            cv2.imshow("window"+str(self.windowName), big_color)

        key = cv2.waitKey(1)
        if key == 27:
            for plugin_name in self.plugins:
                plugin = self.plugins[plugin_name]
                plugin.stop()
            exit(0)
        elif key == ord('s'):
            self.run_surface = not self.run_surface
            self.plugins['plugins.surface'].bypass = self.run_surface
        elif key == ord('y'):
            self.run_yolo = not self.run_yolo
            self.plugins['plugins.yolo'].bypass = self.run_yolo
    
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
            handler = ImageClient(sock, addr)

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
    main()
