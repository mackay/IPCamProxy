import requests

import sys
import traceback

import gevent

from device.camera import StreamingCamera


def stream_generator(url):
    r = requests.get(url, stream=True)
    for chunk in r.iter_content(chunk_size=1024*64):
        yield chunk
        gevent.sleep(0)


def proxy_to_stream(camera):

    def wrapped_proxy_app(environ, start_response):

        headers_out = [
            ("Cache-Control", "no-cache"),
            ("Connection", "close"),
            ("Content-Type", "multipart/x-mixed-replace; boundary=myboundary"),
            ("Expires", "Thu, 01 Dec 1994 16:00:00 GMT"),
            ("Pragma", "no-cache")
        ]

        start_response("200 OK", headers_out)
        return stream_generator("http://" + camera.ip + "/live")

    return wrapped_proxy_app


def create_stream_proxies(app, camera_list):
    for camera in camera_list:
        if isinstance(camera, StreamingCamera):
            print "Stream @ " + "/" + str(camera.ip) + "/live"
            app.mount("/" + camera.ip + "/live", proxy_to_stream(camera))
