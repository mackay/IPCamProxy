import requests

r = requests.get("http://192.168.25.77/live", stream=True)
for content in r.iter_content():
    print r
