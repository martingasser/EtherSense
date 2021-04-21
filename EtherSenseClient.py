#!/usr/bin/python
import sys, getopt
import signal
import asyncio
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
import zmq.asyncio

parser = argparse.ArgumentParser(description='Ethersense client.')
parser.add_argument('--plugins', metavar='N', type=str, nargs='+',
                    help='a list of plugins')
parser.add_argument('--gui', action='store_true')

args = parser.parse_args()

mc_ip_address = '224.0.0.1'

port = 1024
chunk_size = 4096

async def receive_from_zmq(zmq_socket, plugins):

    received_data = {}

    def process_data():
        if 'pose_array' in received_data:
            pose_array = received_data['pose_array']
            translation = pose_array[0:3]
            rotation = pose_array[3:7]
            velocity = pose_array[7:10]
            acceleration = pose_array[10:13]
            angular_velocity = pose_array[13:16]
            angular_acceleration = pose_array[16:19]
        
            translation_text = f'Translation: {translation[0]: 0.2f}, {translation[1]: 0.2f}, {translation[2]: 0.2f}'
            rotation_text = f'Rotation: {rotation[0]: 0.2f}, {rotation[1]: 0.2f}, {rotation[2]: 0.2f}'

            if 'color_array' in received_data:
                color_array = received_data['color_array']
                cv2.putText(color_array, translation_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (65536), 2, cv2.LINE_AA)
                cv2.putText(color_array, rotation_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (65536), 2, cv2.LINE_AA)
            
        if 'yolo_features' in received_data:
            plugin_features = received_data['yolo_features']
            color = (255, 0, 0)
            
            classes = []
            if 'color_array' in received_data:
                for (classname, score, box) in zip(plugin_features['classes'], plugin_features['scores'], plugin_features['boxes']):
                    label = "%s : %f" % (classname, score)
                    cv2.rectangle(self.color_array, box, color, 2)
                    cv2.putText(self.color_array, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        if 'color_array' in received_data:
            if args.gui:
                cv2.imshow("window", received_data['color_array'])

    while True:
        topic, data = await zmq_socket.recv_multipart()
        
        if topic == b'TIME':
            if 'timestamp' in received_data:
                process_data()
            received_data['timestamp'] = struct.unpack('<d', data[0:8])[0]
        elif topic == b'RGB':
            received_data['color_array'] = pickle.loads(data)
        elif topic == b'DEPTH':
            received_data['depth_array'] = pickle.loads(data)
        elif topic == b'POSE':
            received_data['pose_array'] = struct.unpack('<19d', data)
        else:
            plugin_id = topic
            if plugin_id in plugins:
                plugin_features_name = f'{plugin_id.decode()}_features'
                deserialized_features = plugins[plugin_id].deserialize_features(data)
                received_data[plugin_features_name] = deserialized_features

        if args.gui:
            key = cv2.waitKey(1)
            if key == 27:
                break


class DiscoveryClientProtocol:
    def __init__(self, loop):
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        sock = self.transport.get_extra_info('socket')
        sock.settimeout(0)
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        self.transport.sendto(b'ping', (mc_ip_address, port))
        print("Sent ping")

    def datagram_received(self, data, addr):
        print("Reply from {}: {!r}".format(addr, data))

        ctx = zmq.asyncio.Context()
        zmq_socket = ctx.socket(zmq.SUB)
        zmq_socket.connect(f'tcp://{addr[0]}:{addr[1]}')
        
        zmq_socket.subscribe(b'TIME')
        zmq_socket.subscribe(b'RGB')
        zmq_socket.subscribe(b'DEPTH')
        zmq_socket.subscribe(b'POSE')
        zmq_socket.subscribe(b'yolo')

        plugins = []
        if args.plugins:
            plugins = import_plugins(args.plugins)
        
        self.task = asyncio.ensure_future(receive_from_zmq(zmq_socket, plugins))
        self.task.add_done_callback(lambda arg: self.transport.close())
        # Don't close the socket as we might get multiple responses.

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Socket closed, stop the event loop")
        self.loop.stop()



def signal_handler(sig, frame):    
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)

def main():
    loop = asyncio.get_event_loop()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connect = loop.create_datagram_endpoint(
        lambda: DiscoveryClientProtocol(loop),
        sock=sock
    )
    transport, protocol = loop.run_until_complete(connect)
    loop.run_forever()
    transport.close()
    loop.close()    

if __name__ == '__main__':
    main()
