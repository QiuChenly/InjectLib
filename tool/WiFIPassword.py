# -*- encoding: utf-8 -*-
# Author: Zke1ev3n@outlook.com

import sys
import urllib
import urllib.request as urllib2
import json
import hashlib
from Crypto.Cipher import AES
import collections


def getMd5(str):
    md5 = hashlib.md5()
    md5.update(str)
    return md5.hexdigest()


def openwrtWIFIList(radio="radio0"):
    """radio0 和 radio1

    Args:
        radio (str, optional): _description_. Defaults to "radio0".
    """
    u = "http://192.168.55.1/ubus"
    d = (
        '{"jsonrpc":"2.0","id":46,"method":"call","params":["618eaaa669e793ae30e5e7770e324383","iwinfo","scan",{"device":"'
        + radio
        + '"}]}'
    )
    res = urllib2.urlopen(u, d.encode())
    res = res.read()
    res = json.loads(res)
    return res


r0 = openwrtWIFIList()
r1 = openwrtWIFIList("radio1")


dt = collections.OrderedDict()
dt["origChanId"] = "xiaomi"
dt["appId"] = "A0008"
dt["ts"] = "1459936625905"
dt["netModel"] = "w"
dt["chanId"] = "guanwang"
dt["imei"] = "357541051318147"
dt["qid"] = ""
dt["mac"] = "e8:92:a4:9b:16:42"
dt["capSsid"] = "hijack"
dt["lang"] = "cn"
dt["longi"] = "103.985752"
dt["nbaps"] = ""
dt["capBssid"] = "b0:d5:9d:45:b9:85"
dt["bssid"] = "b0:d5:9d:56:82:10"
dt["mapSP"] = "t"
dt["userToken"] = ""
dt["verName"] = "4.1.8"
dt["ssid"] = "360免费WiFi-10"
dt["verCode"] = "3028"
dt["uhid"] = "a0000000000000000000000000000001"
dt["lati"] = "30.579577"
dt["dhid"] = "9374df1b6a3c4072a0271d52cbb2c7b6"
dt = json.dumps(dt, ensure_ascii=False, separators=(",", ":"))
dt = urllib.quote(dt)
j = len(dt)
i = 0
while i < 16 - j % 16:
    dt = dt + " "
    i = i + 1
cipher = AES.new(b"!I50#LSSciCx&q6E", AES.MODE_CBC, b"$t%s%12#2b474pXF")
ed = cipher.encrypt(dt).encode("hex").upper()
data = {}
data["appId"] = "A0008"
data["pid"] = "00300109"
data["ed"] = ed
data["st"] = "m"
data["et"] = "a"
ss = ""
for key in sorted(data):
    ss = ss + data[key]
salt = "*Lm%qiOHVEedH3%A^uFFsZvFH9T8QAZe"
sign = getMd5(ss + salt)
data["sign"] = sign
url = "http://ap.51y5.net/ap/fa.sec"
post_data = urllib.urlencode(data)
req = urllib2.urlopen(url, post_data)
content = req.read()
result = json.loads(content.decode("utf-8"))
if len(result["aps"]) == 0:
    print("Not Found")
    sys.exit()
epwd = result["aps"][0]["pwd"]
cipher = AES.new(b"!I50#LSSciCx&q6E", AES.MODE_CBC, b"$t%s%12#2b474pXF")
pdd = cipher.decrypt(epwd.decode("hex"))
length = int(pdd[:3])
pwd = pdd[3:][:length]
print("password is: " + pwd)
