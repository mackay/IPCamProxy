import requests
from requests.exceptions import ConnectionError
from threading import Thread
from device import ALL_CAMERAS

DEFAULT_NETWORK = "192.168.25"


def do_scan(target_ip, target_cameras, found_ip_container):
    try:
        req = requests.get('http://' + target_ip, timeout=2)

        for camera in target_cameras:
            if camera.is_camera(req.text):
                found_ip_container.append(camera(target_ip))
                break
    except ConnectionError:
        pass

    return


def scan_for_cameras(base_ip_string, target_cameras=ALL_CAMERAS):

    found_cameras = [ ]
    threads = [ ]

    base_ip = ".".join(base_ip_string.split(".")[:3])
    for i in range(256):
        target_ip = base_ip + "." + str(i)
        thread = Thread(target=do_scan, args=(target_ip, target_cameras, found_cameras))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return found_cameras


if __name__ == "__main__":
    print scan_for_cameras(DEFAULT_NETWORK)
