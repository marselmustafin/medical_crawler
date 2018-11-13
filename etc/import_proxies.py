import requests
import re

PROXIES_URL = "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt"
IP_REGEXP = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}\b"

request = requests.get(PROXIES_URL)
downloaded_proxies = re.findall(IP_REGEXP, request.text)

with open("./proxies.txt", "w") as proxies:
    for proxy in downloaded_proxies:
        proxies.write("http://" + proxy + "\n")
