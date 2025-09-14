import os
import sys
try:
    from simple_catalyst_center import CiscoCatalystCenterClient
except ImportError:
    sys.path.insert(0,os.path.sep.join(__file__.split(os.path.sep)[:-1]))
    from simple_catalyst_center import CiscoCatalystCenterClient


import logging
from getpass import getpass
import string
from pprint import pprint
from datetime import datetime,timedelta


IP = input("Please Enter Catalyst Center IP: ") or "100.75.2.2"
username = input("Please Enter Catalyst username: ") or "admin"
password = getpass("Please Enter Catalyst password: ") or "<not set>"


cc = CiscoCatalystCenterClient(f"https://{IP}/", ssl_verify=False)
cc.login(username, password)
api = cc.api

dt_start = datetime.now() - timedelta(minutes=7200)
dt_end = datetime.now() - timedelta(minutes=30)
epoch_start = str(int(dt_start.timestamp())*1000)
epoch_end = str(int(dt_end.timestamp())*1000)

print("Start Date: " + str(dt_start))
print("Start: " + epoch_start)
print("End Date: " + str(dt_end))
print("End: " + epoch_end)

response = cc.api.dna.data.api.v1.clients.query.all(method="POST",body = {
    "startTime": epoch_start,
    "endTime": epoch_end,
	"views":[
		"Detail"
	],
    "page": {
        "limit": 10,
        "offset": 1
    },
	"attributes": [
        "type",
        "username",
        "ipv4Address",
        "vendor",
        "osType",
        "deviceType",
        "siteHierarchyId",
        "usage",
        "connectedNetworkDeviceName",
        "vlanId",
        "band",
        "ssid",
        "protocol"
    ],
	"filters": [
            {
              "key": "type",
              "operator": "eq",
              "value": "Wireless"
            }
	]
})

for client in response:
    print(f"ID: {client['id']}, Site: {client['siteHierarchy']}")

print(len(response))
