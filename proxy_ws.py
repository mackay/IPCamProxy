from bottle import request, abort

import gevent
import websocket
from geventwebsocket import WebSocketError


def proxy_to_ws(ip):
    camera_ws = websocket.WebSocket()
    camera_ws.connect("ws://" + ip + "/ws")

    #this will listen to the camera and return to the client
    def listener(wsock_client):
        while True:
            opcode, message = camera_ws.recv_data()
            wsock_client.send_frame(message, opcode)

    #this will listen to the client and pass on to the camera
    def wrapped_proxy_app(environ, start_response):
        client_ws = request.environ.get('wsgi.websocket')
        if not client_ws:
            abort(400, 'Expected WebSocket request.')

        gevent.spawn(listener, client_ws)

        while True:
            try:
                header, message = client_ws.read_frame()
                camera_ws.send(message, opcode=header.opcode)
            except WebSocketError:
                break

    return wrapped_proxy_app


def create_ws_proxies(app, camera_list):
    for camera in camera_list:
        app.mount("/" + camera + "/ws", proxy_to_ws(camera))
