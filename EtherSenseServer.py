#!/usr/bin/python
import pyrealsense2 as rs
import sys, getopt
import argparse
import asyncore
import numpy as np
import pickle
import socket
import struct
import importlib
from plugins import import_plugins
from threading import Barrier

parser = argparse.ArgumentParser(description='Ethersense client.')
parser.add_argument('--plugins', metavar='N', type=str, nargs='+',
                    help='a list of plugins')
parser.add_argument('--process_async', action='store_true')

parser.add_argument('--osc_ip', default='127.0.0.1')
parser.add_argument('--osc_port', type=int, default=8888)

args = parser.parse_args()


mc_ip_address = '224.0.0.1'
port = 1024
chunk_size = 4096
# rs.log_to_console(rs.log_severity.debug)

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
            # cfg.enable_record_to_file('d435.bag')
            # cfg.enable_device_from_file('d435.bag')
            pipe.start(cfg)
            pipelines['Intel RealSense D435I'] = pipe
        elif 'Intel RealSense T265' in camera_name:
            pipe = rs.pipeline()
            cfg = rs.config()
            cfg.enable_device(detected_camera)
            cfg.enable_stream(rs.stream.pose)
            # cfg.enable_record_to_file('t265.bag')
            # cfg.enable_device_from_file('t265.bag')
            pipe.start(cfg)
            pipelines['Intel RealSense T265'] = pipe
    return pipelines

def get_camera_data(pipelines, image_filter, align):
    frames = pipelines['Intel RealSense D435I'].wait_for_frames()
    aligned_frames = align.process(frames)

    color = aligned_frames.get_color_frame()
    depth = aligned_frames.get_depth_frame()

    frames = pipelines['Intel RealSense T265'].wait_for_frames()
    pose = frames.get_pose_frame()

    if depth and color and pose:
        color_filtered = image_filter.process(color)
        depth_filtered = image_filter.process(depth)
        color_mat = np.asanyarray(color_filtered.as_frame().get_data())
        depth_mat = np.asanyarray(depth_filtered.as_frame().get_data())
        
        pose_data = pose.get_pose_data()
        pose_mat = np.array([
            pose_data.translation.x, pose_data.translation.y, pose_data.translation.z,
            pose_data.rotation.x, pose_data.rotation.y, pose_data.rotation.z
        ])
        ts = frames.get_timestamp()
        return color_mat, depth_mat, pose_mat, ts
    else:
        return None, None           
		
class EtherSenseServer(asyncore.dispatcher):
    def __init__(self, address, pipelines):
        asyncore.dispatcher.__init__(self)

        self.pipelines = pipelines

        self.plugins = {}
        if args.plugins:
            self.barrier = Barrier(len(args.plugins))
            try:
                plugin_classes = import_plugins(args.plugins)
                for plugin_id in plugin_classes:
                    PluginClass = plugin_classes[plugin_id]
                    self.plugins[PluginClass.plugin_id] = PluginClass(process_async=args.process_async, barrier=self.barrier)
            except Exception as ex:
                print(ex)
            


        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        print('sending acknowledgement to', address)
        
	    # reduce the resolution of the depth image using post processing
        self.decimate_filter = rs.decimation_filter()
        self.decimate_filter.set_option(rs.option.filter_magnitude, 2)
        self.frame_data = ''
        self.connect((address[0], 1024))
        self.packet_id = 0

        align_to = rs.stream.color
        self.align = rs.align(align_to)

    def handle_connect(self):
        print("new connection")

    def writable(self):
        return True

    def update_frame(self):
        color, depth, pose, timestamp = get_camera_data(self.pipelines, self.decimate_filter, self.align)
        if depth is not None:

            color_data = pickle.dumps(color)
            depth_data = pickle.dumps(depth)
            pose_data = pickle.dumps(pose)
            color_length = struct.pack('<I', len(color_data))
            depth_length = struct.pack('<I', len(depth_data))
            pose_length = struct.pack('<I', len(pose_data))
	        # include the current timestamp for the frame
            ts = struct.pack('<d', timestamp)

            plugin_frame_data = b''

            for plugin_id in self.plugins:
                plugin = self.plugins[plugin_id]
                results = plugin(color.copy())
                ser = plugin.serialize_features(results[1])
                length_ser = struct.pack('<I', len(ser))
                plugin_frame_data = b''.join([plugin_frame_data, length_ser, ser])


            # color_data = pickle.dumps(color)
            # depth_data = pickle.dumps(depth)
            # pose_data = pickle.dumps(pose)
            # color_length = struct.pack('<I', len(color_data))
            # depth_length = struct.pack('<I', len(depth_data))
            # pose_length = struct.pack('<I', len(pose_data))
	        # # include the current timestamp for the frame
            # ts = struct.pack('<d', timestamp)

            frame_data = b''.join([color_length, depth_length, pose_length, color_data, depth_data, pose_data, plugin_frame_data])
            frame_length = struct.pack('<I', len(frame_data))
            self.frame_data = b''.join([frame_length, frame_data])

    def handle_write(self):
	    # first time the handle_write is called
        if not hasattr(self, 'frame_data'):
            self.update_frame()
	    # the frame has been sent in it entirety so get the latest frame
        if len(self.frame_data) == 0:
	        self.update_frame()
        else:
    	    # send the remainder of the frame_data until there is no data remaining for transmition
            remaining_size = self.send(self.frame_data)
            self.frame_data = self.frame_data[remaining_size:]
	
    def handle_close(self):
        self.close()

class MulticastServer(asyncore.dispatcher):
    def __init__(self, host = mc_ip_address, port=1024):
        asyncore.dispatcher.__init__(self)

        print("Launching Realsense Camera Server")
        try:
            self.pipelines = create_pipelines()
        except:
            print("Unexpected error: ", sys.exc_info()[1])
            sys.exit(1)

        server_address = ('', port)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(server_address)

    def handle_read(self):
        data, addr = self.socket.recvfrom(42)
        print('Received Multicast message %s bytes from %s' % (data, addr))
	    # Once the server recives the multicast signal, open the frame server
        EtherSenseServer(addr, self.pipelines)

    def writable(self): 
        return False # don't want write notifies

    def handle_close(self):
        self.close()

    def handle_accept(self):
        channel, addr = self.accept()
        print('received %s bytes from %s' % (data, addr))


def main(argv):
    server = MulticastServer()
    asyncore.loop()
   
if __name__ == '__main__':
    main(sys.argv[1:])

