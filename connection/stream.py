import requests
import gevent

from device.camera import StreamingCamera
from connection.proxy import clean_headers_for_proxy


def stream_begin(url):
    return requests.get(url, stream=True)


def stream_generator(stream):
    for chunk in stream.iter_content(chunk_size=1024*64):
        yield chunk
        gevent.sleep(0)


def proxy_to_stream(camera):

    def wrapped_proxy_app(environ, start_response):
        url = "http://" + camera.ip + camera.stream_url()
        stream = stream_begin(url)

        headers_in = [ (key, stream.headers[key]) for key in stream.headers ]
        headers_in = clean_headers_for_proxy(headers_in)
        headers_out = camera.cleaner.clean_headers(headers_in, environ, url)

        status = str(stream.status_code) + " " + stream.reason

        start_response(status, headers_out)

        return stream_generator(stream)

    return wrapped_proxy_app


def create_stream_proxies(app, camera_list):
    for camera in camera_list:
        if isinstance(camera, StreamingCamera):
            stream_url = "/" + camera.ip + camera.stream_url()

            print "Stream @ " + stream_url
            app.mount(stream_url, proxy_to_stream(camera))
