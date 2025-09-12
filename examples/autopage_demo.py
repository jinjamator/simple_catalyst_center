import os
try:
    from simple_catalyst_center import CiscoCatalystCenterClient
except ImportError:
    sys.path.insert(0,os.path.sep.join(__file__.split(os.path.sep)[:-1]))
    from simple_catalyst_center import CiscoCatalystCenterClient


import logging
from getpass import getpass
import string
from pprint import pprint

IP = input("Please Enter Catalyst Center IP: ") or "100.75.2.2"
username = input("Please Enter Catalyst username: ") or "admin"
password = getpass("Please Enter Catalyst password: ") or "<not set>"


cc = CiscoCatalystCenterClient(f"https://{IP}/", ssl_verify=False)
cc.login(username, password)
api = cc.api
ids = []

# collect all device ids using all 
for result in api.dna.intent.api.v1("network-device").all(limit=10):
    ids.append(result["id"])

pprint(ids)
print(len(ids))
