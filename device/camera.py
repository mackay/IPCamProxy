
from device.cleaner import Cleaner, InstacamCleaner, IPCamCleaner
from device.targets import INSTACAM, IPCAM

import time


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

    def save_frame(self, path_to_file):
        from selenium import webdriver

        options = webdriver.ChromeOptions()
        options.set_headless(True)
        driver = webdriver.Chrome(chrome_options=options)

        driver.get('http://' + self.ip)
        driver.set_window_size(1280, 800)

        self._save_frame_capture(driver, path_to_file)
        driver.close()
        driver.quit()

    def _save_frame_capture(self, driver, path_to_file):
        time.sleep(1)
        driver.save_screenshot(path_to_file)


class WebsocketCamera(Camera):
    pass


class StreamingCamera(Camera):
    pass


class InstacamCamera(WebsocketCamera):

    DISCOVERY_TOKEN = INSTACAM.DISCOVERY_TOKEN
    CLEANER = InstacamCleaner

    def _save_frame_capture(self, driver, path_to_file):
        time.sleep(2)
        driver.find_element_by_css_selector('#videoCanvas').click()
        driver.save_screenshot(path_to_file)


class IPCamCamera(StreamingCamera):

    DISCOVERY_TOKEN = IPCAM.DISCOVERY_TOKEN
    CLEANER = IPCamCleaner
