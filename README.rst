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