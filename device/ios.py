import time
import gzip
from StringIO import StringIO

from device.camera import WebsocketCamera, StreamingCamera
from device.cleaner import Cleaner


class InstacamCleaner(Cleaner):
    URL_TOKEN = "instacam.amalgamation.js"
    CONTENT_TOKEN = None

    def __init__(self):
        super(InstacamCleaner, self).__init__(target_url_token=self.URL_TOKEN, target_content_token=self.CONTENT_TOKEN)

    def clean_content(self, content, environ):
        content = gzip.GzipFile(fileobj=StringIO(content)).read()
        content = content.replace("var address = 'ws://' + window.location.host + '/ws';",
                                  "var address = 'ws://' + window.location.href.split('//')[1] + 'ws';")

        out = StringIO()
        with gzip.GzipFile(fileobj=out, mode="w") as f:
            f.write(content)

        return super(InstacamCleaner, self).clean_content(out.getvalue(), environ)

    def clean_headers(self, headers, environ, url=None, content=None):
        adjusted_headers = headers

        if url and self.URL_TOKEN in url:
            adjusted_headers = [ ]
            for header in headers:
                if header[0].lower() == "content-length":
                    adjusted_headers.append( ("Content-Length", "61505") )
                else:
                    adjusted_headers.append(header)

        return super(InstacamCleaner, self).clean_headers(adjusted_headers, environ, url=url, content=content)


class InstacamCamera(WebsocketCamera):
    DISCOVERY_TOKEN = "instacam.amalgamation.js"
    CLEANER = InstacamCleaner

    def _save_frame_capture(self, driver, path_to_file):
        time.sleep(2)
        driver.find_element_by_css_selector('#videoCanvas').click()
        driver.save_screenshot(path_to_file)


class IPCamCleaner(Cleaner):
    URL_TOKEN = None
    CONTENT_TOKEN = "<title>iPCamera for iOS</title>"

    def __init__(self):
        super(IPCamCleaner, self).__init__(target_url_token=self.URL_TOKEN, target_content_token=self.CONTENT_TOKEN)

    def clean_content(self, content, environ):
        content = content.replace("<script type=\"text/javascript\" src=\"/jquery-1.8.2.min.js\"></script>",
                                  "<script type=\"text/javascript\" src=\"jquery-1.8.2.min.js\"></script>" )

        content = content.replace("$.getJSON(\"/parameters",
                                  "$.getJSON(\"parameters")

        content = content.replace("$(\"#live\").attr(\"src\", \"/live\");",
                                  "$(\"#live\").attr(\"src\", \"live\");")

        return super(IPCamCleaner, self).clean_content(content, environ)

    def clean_headers(self, headers, environ, url=None, content=None):
        return super(IPCamCleaner, self).clean_headers(headers, environ, url=url, content=content)


class IPCamCamera(StreamingCamera):

    DISCOVERY_TOKEN = "<title>iPCamera for iOS</title>"
    CLEANER = IPCamCleaner
