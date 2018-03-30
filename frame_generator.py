#!/usr/bin/python

# pip install...
#   wsgiprox[gevent-websocket]
#   bottle
#   websocket-client
import os
import errno
import time

from device.scan import scan_for_cameras, DEFAULT_NETWORK
from PIL import Image


import argparse


def capture_screens(cameras, file_location="./"):
    for camera in cameras:
        try:
            camera.save_frame(file_location + str(camera.ip) + ".png")
        except:
            #if we fail to save the frame, we just move on
            continue

        im = Image.open(file_location + str(camera.ip) + ".png")
        rgb_im = im.convert('RGB')
        rgb_im.save(file_location + str(camera.ip) + ".jpg", quality=75)

        rgb_im.thumbnail((300, 300), Image.ANTIALIAS)
        rgb_im.save(file_location + str(camera.ip) + "_thumbnail.jpg", quality=75)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--network", default=DEFAULT_NETWORK)
    parser.add_argument("--path", default="./frames")
    parser.add_argument("--interval", type=int, default=10)
    args = parser.parse_args()

    network = args.network
    frame_location = args.path

    #make sure the frame location exists
    if frame_location[0] != "/":
        frame_location += "/"

    try:
        os.makedirs(frame_location)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    #grab frames
    while True:
        cameras = scan_for_cameras(network)
        print "Found Cameras: " + str(cameras)

        capture_screens(cameras, file_location=frame_location)

        time.sleep(args.interval)
