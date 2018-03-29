import requests
from threading import Thread

DEFAULT_NETWORK = "192.168.25"


def do_scan(target_ip, target_token, found_ip_container):
    try:
        req = requests.get('http://' + target_ip, timeout=2)

        if target_token in req.text:
            found_ip_container.append(target_ip)
    except:
        pass

    return


def scan_for_cameras(base_ip_string, target_token="instacam.amalgamation.js"):
    found_cameras = [ ]
    threads = [ ]

    base_ip = ".".join(base_ip_string.split(".")[:3])
    for i in range(256):
        target_ip = base_ip + "." + str(i)
        thread = Thread(target=do_scan, args=(target_ip, target_token, found_cameras))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return found_cameras

if __name__ == "__main__":
    print scan_for_cameras(DEFAULT_NETWORK)
