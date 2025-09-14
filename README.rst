Introduction
==================

simple_catalyst_center is a simplified REST Client for the Cisco Catalyst Center (formerly known as DNA Center).



Features
-----------------

simple_catalyst_center has following features:
    * manage login
    * download files
    * wait for task results
    * CRUD interface for all possible API URLs

Installation
------------

Install simple_catalyst_center by running:

.. code-block:: bash

    pip3 install simple_catalyst_center


Examples
---------

get backup zip file for all devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    from simple_catalyst_center import CiscoCatalystCenterClient
    import logging
    from getpass import getpass
    import secrets
    import string

    logger = logging.getLogger()
    logging.basicConfig(encoding="utf-8", level=logging.INFO)


    IP=input("Please Enter Catalyst Center IP: ") or "100.75.2.2"
    username=input("Please Enter Catalyst username: ") or "admin"
    password=getpass("Please Enter Catalyst password: ") or "not set"
    zip_password=input("Please Enter ZIP password: ") 
    if not zip_password:
        zip_password=''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(12)))
        print(f"generated zip password is: {zip_password}")


    cc = CiscoCatalystCenterClient(f"https://{IP}/", ssl_verify=False)
    cc.login(username, password) 
    api=cc.api
    ids=[]

    # collect all device ids
    for result in api.dna.intent.api.v1("network-device").get(params={"managementIpAddress": ["100.75.1.11"]}):
        ids.append(result["id"])
        

    res=api.dna.intent.api.v1("network-device-archive").cleartext.post(body={
        "deviceId": ids,
        "password": zip_password
    })

    # download task result, needs task URL and target filename

    cc.download(res.get("url"), res.get("taskId") + ".zip")

use autopaging with GET
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

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
    for result in api.dna.intent.api.v1("network-device").all(limit=10): #default limit is 500
        ids.append(result["id"])

    pprint(ids)
    print(len(ids))

use autopaging with POST
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python


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




Contribute
----------

- Issue Tracker: https://github.com/jinjamator/simple_catalyst_center/issues
- Source Code: https://github.com/jinjamator/simple_catalyst_center

Roadmap
-----------------

Selected Roadmap items:
    * add more documentation
    * add some more examples

For documentation please refer to https://simple_catalyst_center.readthedocs.io/en/latest/

License
-----------------

This project is licensed under the Apache License Version 2.0