# import time
from device.camera import StreamingCamera
from device.cleaner import Cleaner


class IPWebcamCleaner(Cleaner):
    URL_TOKEN = "ipwebcam.js"
    CONTENT_TOKEN = "var root = '';"

    def __init__(self):
        super(IPWebcamCleaner, self).__init__(target_url_token=self.URL_TOKEN, target_content_token=self.CONTENT_TOKEN)

    def clean_content(self, content, environ):
        content = content.replace("var root = '';",
                                  "var root = '.';" )

        return super(IPWebcamCleaner, self).clean_content(content, environ)


class IPWebcam(StreamingCamera):

    DISCOVERY_TOKEN = "<p>&copy; Pavel Khlebovich 2013</p>"
    CLEANER = IPWebcamCleaner

    def _save_frame_url(self):
        return 'http://' + self.ip + "/video"

    def stream_url(self):
        return "/video"
