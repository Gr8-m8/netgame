from networkagent import NetworkAgent

import requests
ip = requests.get("https://api.ipify.org/?format=json").json()['ip']
port = "7777"
NetworkAgent.SaveConnectionData(ip, port)
print(f"{ip}:{port}")