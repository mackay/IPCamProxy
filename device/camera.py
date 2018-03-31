
from device.cleaner import Cleaner
import time


class Camera(object):
    DISCOVERY_TOKEN = "Unknown"
    CLEANER = Cleaner

    @classmethod
    def is_camera(cls, content):
        return cls.DISCOVERY_TOKEN in content

    def __init__(self, ip):
        self.ip = ip

    def __repr__(self):
        return str(self.ip)

    @property
    def cleaner(self):
        return self.CLEANER()

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
