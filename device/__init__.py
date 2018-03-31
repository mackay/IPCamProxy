
from device.ios import InstacamCamera, IPCamCamera
from device.android import IPWebcam

ALL_CAMERAS = [ InstacamCamera, IPCamCamera, IPWebcam ]
IOS_CAMERAS = [ InstacamCamera, IPCamCamera ]
ANDROID_CAMERAS = [ IPWebcam ]


from device.ios import InstacamCleaner, IPCamCleaner
from device.android import IPWebcamCleaner

ALL_CLEANERS = [ InstacamCleaner, IPCamCleaner, IPWebcamCleaner ]
IOS_CLEANERS = [ InstacamCleaner, IPCamCleaner ]
ANDROID_CLEANERS = [ IPWebcamCleaner ]


class CameraRegistry(object):

    def __init__(self):
        self.cameras = [ ]

    def clear(self):
        self.cameras = [ ]

    def add(self, camera):
        self.cameras.append(camera)


REGISTERED_DEVICES = CameraRegistry()
