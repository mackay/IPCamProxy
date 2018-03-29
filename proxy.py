from urllib import quote as url_quote
import wsgiproxy.exactproxy

import gzip
from StringIO import StringIO

CLEAN_TARGET = "instacam.amalgamation.js"
CLEAN_TARGET_ENVIRON_SIZE_KEY = "x-instacam.amalgamation.js-size"


#we're going to monkey-patch proxy_exact_request ...
proxy_exact_request = wsgiproxy.exactproxy.proxy_exact_request


#... with this function to adjust the js coming from the app
def intercept_and_clean_js(environ, start_response):
    result = proxy_exact_request(environ, start_response)

    path = (url_quote(environ.get('SCRIPT_NAME', '')) + url_quote(environ.get('PATH_INFO', '')))

    if CLEAN_TARGET in path:
        content = gzip.GzipFile(fileobj=StringIO(result[0])).read()
        content = content.replace("var address = 'ws://' + window.location.host + '/ws';",
                                  "var address = 'ws://' + window.location.href.split('//')[1] + 'ws';")

        out = StringIO()
        with gzip.GzipFile(fileobj=out, mode="w") as f:
            f.write(content)
        result[0] = out.getvalue()

        environ[CLEAN_TARGET_ENVIRON_SIZE_KEY] = str(len(result[0]))

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


def wrap_start_response(environ, start_response):
    def wrapped_start_response(status, headers_out):
        # Remove "hop-by-hop" headers
        headers_out = [(k, v) for (k, v) in headers_out if k not in FILTER_HEADERS]
        adjusted_headers = headers_out

        path = (url_quote(environ.get('SCRIPT_NAME', '')) + url_quote(environ.get('PATH_INFO', '')))
        if CLEAN_TARGET in path:
            adjusted_headers = [ ]
            for header in headers_out:
                if header[0].lower() == "content-length":
                    adjusted_headers.append(("Content-Length",
                                             environ.get(CLEAN_TARGET_ENVIRON_SIZE_KEY, "61505") ))
                else:
                    adjusted_headers.append(header)

        return start_response(status, adjusted_headers)
    return wrapped_start_response


def proxy_to_camera(ip):
    proxy_app = WSGIProxyApp("http://" + ip)

    def wrapped_proxy_app(environ, start_response):
        start_response = wrap_start_response(environ, start_response)
        return proxy_app(environ, start_response)

    return wrapped_proxy_app


def create_camera_proxies(app, camera_list):
    for camera in camera_list:
        app.mount("/" + camera, proxy_to_camera(camera))
