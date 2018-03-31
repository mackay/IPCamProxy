
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

    @property
    def safe_filename(self):
        return str(self.ip).replace(":", "_")

    def save_frame(self, path_to_file):
        driver = self._save_frame_driver()
        driver.get(self._save_frame_url())
        driver.set_window_size(1280, 800)

        self._save_frame_capture(driver, path_to_file)
        driver.close()
        driver.quit()

    def _save_frame_driver(self):
        from selenium import webdriver

        options = webdriver.ChromeOptions()
        options.set_headless(True)
        driver = webdriver.Chrome(chrome_options=options)

        return driver

    def _save_frame_url(self):
        return 'http://' + self.ip

    def _save_frame_capture(self, driver, path_to_file):
        time.sleep(1)
        driver.save_screenshot(path_to_file)


class WebsocketCamera(Camera):

    def socket_url(self):
        raise


class StreamingCamera(Camera):

    def stream_url(self):
        raise


    def _save_frame_driver(self):
        from selenium import webdriver
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

        options = webdriver.ChromeOptions()
        options.set_headless(True)

        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["pageLoadStrategy"] = "none"

        driver = webdriver.Chrome(chrome_options=options, desired_capabilities=capabilities)

        return driver
