#!/usr/bin/python

# pip install...
#   wsgiprox[gevent-websocket]
#   bottle
#   websocket-client
from gevent import monkey
monkey.patch_all()

import bottle
from bottle import auth_basic, view, redirect
from bottle import static_file
from bottle import request

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from passlib.hash import sha256_crypt

from util.users import USER_REGISTRY
from device.scan import scan_for_cameras, DEFAULT_NETWORK
from connection.proxy import create_camera_proxies
from connection.socket import create_ws_proxies
from connection.stream import create_stream_proxies

#have some basic logging to the screen
import logging
logging.basicConfig(format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger()
log.setLevel(logging.INFO)

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
    create_proxies()

    redirect("/")


@app.route('/frames/<filename>', method='GET')
@auth_basic(check_pass)
def get_frame(filename):
    return static_file(filename, root="./frames")


@app.hook('after_request')
def after_request():
    log.info("LEAVE: {1} {0} {2}".format(request.path, request.method, request.query_string))


@app.hook('before_request')
def before_request():
    log.info("ENTER: {1} {0} {2}".format(request.path, request.method, request.query_string))


def create_proxies():
    global cameras
    global network
    global app

    cameras = scan_for_cameras(network)

    create_camera_proxies(app, cameras)
    create_ws_proxies(app, cameras)
    create_stream_proxies(app, cameras)


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--host", default="localhost")
parser.add_argument("--port", type=int, default=8080)
parser.add_argument("--network", default=DEFAULT_NETWORK)
args = parser.parse_args()

network = args.network
create_proxies()

print "Server On: " + str(args.host) + ":" + str(args.port)
print "Using Network: " + network
print "Found Cameras: " + str(cameras)

server = WSGIServer((args.host, args.port), app,
                    handler_class=WebSocketHandler
                    # ,keyfile='server.key', certfile='server.crt'
                    )
server.serve_forever()
