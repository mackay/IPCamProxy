from bottle import request, abort

import gevent
import websocket

from device.camera import WebsocketCamera


def proxy_to_ws(camera):

    class CameraProxy(object):

        def __init__(self, environ, start_response):
            self.environ = environ
            self.start_response = start_response
            self.run_threads = True

            self.wrapped_proxy_app(environ, start_response)

        def wrapped_proxy_app(self, environ, start_response):
            camera_ws = websocket.WebSocket()
            camera_ws.connect("ws://" + camera.ip + "/ws")

            client_ws = request.environ.get('wsgi.websocket')
            if not client_ws:
                abort(400, 'Expected WebSocket request.')

            threads = [ gevent.spawn(self.listener, client_ws, camera_ws),
                        gevent.spawn(self.sender, client_ws, camera_ws) ]

            gevent.joinall( threads )

            camera_ws.close()
            client_ws.close()

        #this will listen to the camera and return to the client
        def listener(self, wsock_client, wsock_camera):
            while self.run_threads:
                try:
                    opcode, message = wsock_camera.recv_data()
                    wsock_client.send_frame(message, opcode)
                except:
                    self.run_threads = False
                    break

        #this will listen to the client and pass on to the camera
        def sender(self, wsock_client, wsock_camera):
            while self.run_threads:
                try:
                    header, message = wsock_client.read_frame()
                    wsock_camera.send(message, opcode=header.opcode)
                except:
                    self.run_threads = False
                    break

    return CameraProxy


def create_ws_proxies(app, camera_list):
    for camera in camera_list:
        if isinstance(camera, WebsocketCamera):
            socket_url = "/" + str(camera.ip) + camera.socket_url()

            print "Socket @ " + socket_url
            app.mount(socket_url, proxy_to_ws(camera))
