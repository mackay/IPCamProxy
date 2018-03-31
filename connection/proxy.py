from urllib import quote as url_quote
import wsgiproxy.exactproxy

#in order to process each camera's js/html/app files ...
ENVIRON_CAMERA_KEY = "x-camera"


#... we're going to monkey-patch proxy_exact_request ...
proxy_exact_request = wsgiproxy.exactproxy.proxy_exact_request


#... with this function to adjust the js coming from the app
def intercept_and_clean_js(environ, start_response):
    result = proxy_exact_request(environ, start_response)
    path = (url_quote(environ.get('SCRIPT_NAME', '')) + url_quote(environ.get('PATH_INFO', '')))

    camera = environ.get(ENVIRON_CAMERA_KEY, None)
    if camera and camera.cleaner.is_target(path, result[0]):
        result[0] = camera.cleaner.clean_content(result[0], environ)

    return result


# ... and finish the patching here
wsgiproxy.exactproxy.proxy_exact_request = intercept_and_clean_js


#include this AFTER monkey patching - if we include before it will all be for naught
from wsgiproxy.app import WSGIProxyApp


# Remove "hop-by-hop" headers (as defined by RFC2613, Section 13)
# since they are not allowed by the WSGI standard.
FILTER_HEADERS = [
    'Connection',
    'Keep-Alive',
    'Proxy-Authenticate',
    'Proxy-Authorization',
    'TE',
    'Trailers',
    'Transfer-Encoding',
    'Upgrade',
    ]


def clean_headers_for_proxy(headers):
    # Remove "hop-by-hop" headers
    return [(k, v) for (k, v) in headers if k not in FILTER_HEADERS]


def wrap_start_response(camera, environ, start_response):

    #this will be our hook back to the camera in the proxy
    environ[ENVIRON_CAMERA_KEY] = camera

    def wrapped_start_response(status, headers_out):
        adjusted_headers = clean_headers_for_proxy(headers_out)

        path = (url_quote(environ.get('SCRIPT_NAME', '')) + url_quote(environ.get('PATH_INFO', '')))
        adjusted_headers = camera.cleaner.clean_headers(headers_out, environ, url=path)

        return start_response(status, adjusted_headers)
    return wrapped_start_response


def proxy_to_camera(camera):
    proxy_app = WSGIProxyApp("http://" + camera.ip)

    def wrapped_proxy_app(environ, start_response):
        start_response = wrap_start_response(camera, environ, start_response)
        return proxy_app(environ, start_response)

    return wrapped_proxy_app


def create_camera_proxies(app, camera_list):
    for camera in camera_list:
        app.mount("/" + camera.ip, proxy_to_camera(camera))
