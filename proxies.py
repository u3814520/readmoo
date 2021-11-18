import requests
import re

res = requests.get('https://free-proxy-list.net/')
m = re.findall('\d+\.\d+\.\d+\.\d+:\d+', res.text)
validips = []
for ip in m:
    try:
        res = requests.get('https://api.ipify.org?format=json', proxies={'http': ip, 'https': ip}, timeout = 5 )
        validips.append({'ip': ip})
        print(res.json())
    except:
        print("FAIL:", ip)
