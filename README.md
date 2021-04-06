# RealSense client/server architecture

Ethernet client and server for RealSense using python's Asyncore.

Based on code by [Philip Krejov](http://www.krejov.com).

## Prerequisites

Installation and Setup of Server:

```
sudo python setup.py
```

This will first install the pip dependencies, followed by the creation of cronjobs in the /etc/crontab file that maintains an instance of the Server running whenever the device is powered.

## Overview

Mulicast broadcast is used to establish connections to servers that are present on the network. 
Once a server receives a request for connection from a client, Asyncore is used to establish a TCP connection for each server. 
Frames are collected from the camera using librealsense pipeline. It is then resized and send in smaller chucks as to conform with TCP.

## Error Logging

Errors are piped to a log file stored in /tmp/error.log as part of the command that is setup in /etc/crontab

### Network bandwidth

It is currently very easy to saturate the bandwidth of the Ethernet connection I have tested 5 servers connected to the same client without issue beyond limited framerate:

cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

self.decimate_filter.set_option(rs.option.filter_magnitude, 2)

There are a number of strategies that can be used to increase this bandwidth but are left to the user for brevity and the specific tradeoff for your application, these include:

Transmitting frames using UDP and allowing for frame drop, this requires implementation of packet ordering.

Reducing the depth channel to 8bit.

Reducing the resolution further.

The addition of compression, either frame wise or better still temporal.

Local recording of the depth data into a buffer, with asynchronous frame transfer.

## TroubleShooting Tips

Check that the server is running on the device using "ps -eaf | grep "python EtherSenseServer.py"

Finally check the log file at /tmp/error.log

There might still be some conditions where the Server is running but not in a state to transmit, help in narrowing these cases would be much appreciated. 
