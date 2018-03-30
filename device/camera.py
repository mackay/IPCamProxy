
from device.cleaner import Cleaner, InstacamCleaner, IPCamCleaner

from device.targets import INSTACAM, IPCAM


class Camera(object):

    DISCOVERY_TOKEN = "Unknown"
    CLEANER = Cleaner

    @classmethod
    def is_camera(cls, content):
        return cls.DISCOVERY_TOKEN in content

    def __init__(self, ip):
        self.ip = ip

    def cleaner(self):
        return self.CLEANER()

    def __repr__(self):
        return str(self.ip)


class WebsocketCamera(Camera):
    pass


class StreamingCamera(Camera):
    pass


class InstacamCamera(WebsocketCamera):

    DISCOVERY_TOKEN = INSTACAM.DISCOVERY_TOKEN
    CLEANER = InstacamCleaner


class IPCamCamera(StreamingCamera):

    DISCOVERY_TOKEN = IPCAM.DISCOVERY_TOKEN
    CLEANER = IPCamCleaner
