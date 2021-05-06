#!/usr/bin/python
import pyrealsense2 as rs
import sys, getopt
import argparse
import asyncio
import numpy as np
import pickle
import socket
import struct
import importlib
from plugins import import_plugins
from threading import Barrier
import zmq
import zmq.asyncio
import math as m


parser = argparse.ArgumentParser(description='Ethersense client.')
parser.add_argument('--plugins', metavar='N', type=str, nargs='+',
                    help='a list of plugins')
parser.add_argument('--process_async', action='store_true')

args = parser.parse_args()

mc_ip_address = '224.0.0.1'
port = 1024
chunk_size = 4096

def create_pipelines():
    ctx = rs.context()
    devices = ctx.query_devices()
    
    pipelines = {}

    for device_id in range(devices.size()):
        device = devices[device_id]
        detected_camera = device.get_info(rs.camera_info.serial_number)
        camera_name = device.get_info(rs.camera_info.name)
        del device

        print(f'Detected {camera_name}, Serial: {detected_camera}')

        if 'Intel RealSense D435I' in camera_name:
            pipe = rs.pipeline()
            cfg = rs.config()
            cfg.enable_device(detected_camera)
            cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
            cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
            pipe.start(cfg)
            pipelines['Intel RealSense D435I'] = pipe
        elif 'Intel RealSense T265' in camera_name:
            pipe = rs.pipeline()
            cfg = rs.config()
            cfg.enable_device(detected_camera)
            cfg.enable_stream(rs.stream.pose)
            pipe.start(cfg)
            pipelines['Intel RealSense T265'] = pipe
    return pipelines

def get_camera_data(pipelines, image_filter, align):
    frames = pipelines['Intel RealSense D435I'].wait_for_frames()
    aligned_frames = align.process(frames)

    color = aligned_frames.get_color_frame()
    depth = aligned_frames.get_depth_frame()

    # frames = pipelines['Intel RealSense T265'].wait_for_frames()
    # pose = frames.get_pose_frame()

    # if depth and color and pose:
    if depth and color:
        color_filtered = image_filter.process(color)
        depth_filtered = image_filter.process(depth)

        color_mat = np.asanyarray(color_filtered.as_frame().get_data())
        depth_mat = np.asanyarray(depth_filtered.as_frame().get_data())

        '''
        pose_data = pose.get_pose_data()
        
        x = pose_data.rotation.x
        y = pose_data.rotation.y
        z = pose_data.rotation.z
        w = pose_data.rotation.w

        pitch =  -m.asin(2.0 * (x*z - w*y)) * 180.0 / m.pi
        yaw   =  m.atan2(2.0 * (w*z + x*y), w*w + x*x - y*y - z*z) * 180.0 / m.pi
        roll  =  m.atan2(2.0 * (w*x + y*z), w*w - x*x - y*y + z*z) * 180.0 / m.pi

        pose_mat = np.array([
            pose_data.translation.x, pose_data.translation.y, pose_data.translation.z,
            pitch, yaw, roll,
            pose_data.velocity.x, pose_data.velocity.y, pose_data.velocity.z,
            pose_data.acceleration.x, pose_data.acceleration.y, pose_data.acceleration.z,
            pose_data.angular_velocity.x, pose_data.angular_velocity.y, pose_data.angular_velocity.z,
            pose_data.angular_acceleration.x, pose_data.angular_acceleration.y, pose_data.angular_acceleration.z
        ])
        ts = frames.get_timestamp()
        return color_mat, depth_mat, pose_mat, ts
        '''

        ts = frames.get_timestamp()
        return color_mat, depth_mat, ts
    else:
        return None, None           


async def stream_data(pipelines, decimate_filter, align, zmq_socket, plugins):
    while (True):
        # color, depth, pose, timestamp = get_camera_data(pipelines, decimate_filter, align)
        color, depth, timestamp = get_camera_data(pipelines, decimate_filter, align)

        color_data = pickle.dumps(color)
        depth_data = pickle.dumps(depth)
        #pose_data = struct.pack('<18d', *pose.tolist())

        ts = struct.pack('<d', timestamp)

        await zmq_socket.send_multipart([b'TIME', ts])
        await zmq_socket.send_multipart([b'RGB', color_data])
        await zmq_socket.send_multipart([b'DEPTH', depth_data])
        #await zmq_socket.send_multipart([b'POSE', pose_data])

        plugin_frame_data = b''

        for plugin_id in plugins:
            plugin = plugins[plugin_id]
            results = plugin(color.copy())
            if results is not None:
                features = results[1]
                ser = plugin.serialize_features(features)
                await zmq_socket.send_multipart([plugin.plugin_id, ser])

        await asyncio.sleep(0)

class MulticastServerProtocol:

    def __init__(self, loop):

        print("Launching Realsense Camera Server")
        try:
            self.pipelines = create_pipelines()
            #if len(self.pipelines) != 2:
            #    print('couldn\'t find Realsense devices.')
        except:
            print("Unexpected error: ", sys.exc_info()[1])
            sys.exit(1)

        self.plugins = {}
        if args.plugins:
            self.barrier = Barrier(len(args.plugins))
            try:
                plugin_classes = import_plugins(args.plugins)
                for plugin_id in plugin_classes:
                    PluginClass = plugin_classes[plugin_id]
                    self.plugins[PluginClass.plugin_id] = PluginClass(process_async=args.process_async, barrier=self.barrier)
                    print(f'Loaded plugin {plugin_id.decode()}')
            except Exception as ex:
                print(ex)

        self.decimate_filter = rs.decimation_filter()
        self.decimate_filter.set_option(rs.option.filter_magnitude, 2)
        self.frame_data = ''

        align_to = rs.stream.color
        self.align = rs.align(align_to)

        ctx = zmq.asyncio.Context()
        zmq_socket = ctx.socket(zmq.PUB)
        zmq_socket.bind("tcp://*:%d" % port)
        self.stream_task = asyncio.ensure_future(stream_data(self.pipelines, self.decimate_filter, self.align, zmq_socket, self.plugins))

        
    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        self.stream_task.cancel()

    def datagram_received(self, data, addr):
        self.transport.sendto(b'pong', addr)

import signal
import sys

def main(argv):
    loop = asyncio.get_event_loop()
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_address = ('', port)
    sock.bind(server_address)

    connect = loop.create_datagram_endpoint(
        lambda: MulticastServerProtocol(loop),
        sock=sock
    )

    transport, protocol = loop.run_until_complete(connect)

    def shutdown_handler():
        loop.stop()
    loop.add_signal_handler(signal.SIGINT, shutdown_handler)

    try:
        loop.run_forever()
    finally:
        transport.close()
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
   
if __name__ == '__main__':
    main(sys.argv[1:])
