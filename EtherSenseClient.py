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

async def receive_from_zmq(zmq_socket, plugins, queue):
    received_data = {}
    while True:
        try:
            topic, data = await zmq_socket.recv_multipart()
            if topic == b'TIME':
                if 'timestamp' in received_data:
                    #res = process_data()
                    queue.put_nowait(received_data)
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

        except asyncio.CancelledError:
            print('cancelled')
            raise
    
    loop = asyncio.get_running_loop()
    loop.stop()

async def send_ping(transport, address):
    while True:
        try:
            transport.sendto(b'ping', address)
            print(f'Sent ping to {str(address)}')
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            raise

def process_display_data(received_data):
    if 'pose_array' in received_data:
        pose_array = received_data['pose_array']
        translation = pose_array[0:3]
        rotation = pose_array[3:7]
        velocity = pose_array[7:10]
        acceleration = pose_array[10:13]
        angular_velocity = pose_array[13:16]
        angular_acceleration = pose_array[16:19]
    
        translation_text = f'Translation: {translation[0]: 0.2f}, {translation[1]: 0.2f}, {translation[2]: 0.2f}'
        rotation_text = f'Rotation: {rotation[0]: 0.2f}, {rotation[1]: 0.2f}, {rotation[2]: 0.2f}, {rotation[3]: 0.2f}'

        if 'color_array' in received_data:
            color_array = received_data['color_array']
            cv2.putText(color_array, translation_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (65536), 2, cv2.LINE_AA)
            cv2.putText(color_array, rotation_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (65536), 2, cv2.LINE_AA)
        
    if 'yolo_features' in received_data:
        plugin_features = received_data['yolo_features']
        color = (255, 0, 0)
        
        classes = []
        if 'color_array' in received_data:
            color_array = received_data['color_array']
            for (classname, score, box) in zip(plugin_features['classes'], plugin_features['scores'], plugin_features['boxes']):
                label = "%s : %f" % (classname, score)
                cv2.rectangle(color_array, box, color, 2)
                cv2.putText(color_array, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return color_array


async def display_data(queue):
    while True:
        received_data = await queue.get()
        color_array = process_display_data(received_data)
        if args.gui:
            cv2.imshow("window", color_array)
            key = cv2.waitKey(1)
            # if key == 27:
            #     break
        queue.task_done()


class DiscoveryClientProtocol:
    def __init__(self, loop):
        self.loop = loop
        self.transport = None
        self.ctx = None
        
        self.display_task = None

    def connection_made(self, transport):
        self.transport = transport
        sock = self.transport.get_extra_info('socket')
        sock.settimeout(0)
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        self.ping_task = asyncio.ensure_future(send_ping(self.transport, (mc_ip_address, port)))

    def datagram_received(self, data, addr):
        print("Received {!r} from {}".format(data, addr))

        if self.ctx is None:
            self.ctx = zmq.asyncio.Context()
            zmq_socket = self.ctx.socket(zmq.SUB)
            zmq_socket.connect(f'tcp://{addr[0]}:{addr[1]}')
            
            zmq_socket.subscribe(b'TIME')
            zmq_socket.subscribe(b'RGB')
            zmq_socket.subscribe(b'DEPTH')
            zmq_socket.subscribe(b'POSE')
            zmq_socket.subscribe(b'yolo')

            plugins = []
            if args.plugins:
                plugins = import_plugins(args.plugins)
            
            queue = asyncio.Queue()
            self.receive_task = asyncio.ensure_future(receive_from_zmq(zmq_socket, plugins, queue))
            if args.gui:
                self.display_task = asyncio.ensure_future(display_data(queue))

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        if self.ping_task:
            self.ping_task.cancel()
        if self.receive_task:
            self.receive_task.cancel()
        if self.display_task:
            self.display_task.cancel()


def main():
    loop = asyncio.get_event_loop()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connect = loop.create_datagram_endpoint(
        lambda: DiscoveryClientProtocol(loop),
        sock=sock
    )
    transport, protocol = loop.run_until_complete(connect)

    def signal_handler():
        loop.stop()
        
    loop.add_signal_handler(signal.SIGINT, signal_handler )

    try:
        loop.run_forever()
    finally:
        transport.close()
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()    

if __name__ == '__main__':
    main()
