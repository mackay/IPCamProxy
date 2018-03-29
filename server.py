# pip install...
#   wsgiprox[gevent-websocket]
#   bottle
#   websocket-client

import bottle
from bottle import auth_basic, view, redirect

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from passlib.hash import sha256_crypt

from users import USER_REGISTRY
from scan import scan_for_cameras, DEFAULT_NETWORK
from proxy import create_camera_proxies
from proxy_ws import create_ws_proxies


#default server characteristics
app = bottle.Bottle()
network = DEFAULT_NETWORK

#the global placeholder for discovered camera IPs
cameras = [ ]


def check_pass(username, password, salt=None):
    user = USER_REGISTRY.get_user(username)
    if user:
        return sha256_crypt.verify(user.salt + password, user.hash)

    return False


@app.route('/', method='GET')
@auth_basic(check_pass)
@view('index')
def index():
    global cameras
    return { "cameras": cameras }


@app.route('/recycle', method='GET')
@auth_basic(check_pass)
@view('index')
def recycle():
    global cameras
    global network
    cameras = scan_for_cameras(network)
    create_camera_proxies(app, cameras)
    create_ws_proxies(app, cameras)

    redirect("/")


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--host", default="localhost")
parser.add_argument("--port", type=int, default=8080)
parser.add_argument("--network", default=DEFAULT_NETWORK)
args = parser.parse_args()

network = args.network

cameras = scan_for_cameras(network)
create_camera_proxies(app, cameras)
create_ws_proxies(app, cameras)

server = WSGIServer((args.host, args.port), app,
                    handler_class=WebSocketHandler
                    # ,keyfile='server.key', certfile='server.crt'
                    )
server.serve_forever()
