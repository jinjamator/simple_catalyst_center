from simple_catalyst_center import CiscoCatalystCenterClient
import logging
from getpass import getpass
import secrets
import string

logger = logging.getLogger()
logging.basicConfig(encoding="utf-8", level=logging.INFO)


IP = input("Please Enter Catalyst Center IP: ") or "100.75.2.2"
username = input("Please Enter Catalyst username: ") or "admin"
password = getpass("Please Enter Catalyst password: ") or "not set"
zip_password = input("Please Enter ZIP password: ")
if not zip_password:
    zip_password = "".join(
        (
            secrets.choice(string.ascii_letters + string.digits + string.punctuation)
            for i in range(12)
        )
    )
    print(f"generated zip password is: {zip_password}")


cc = CiscoCatalystCenterClient(f"https://{IP}/", ssl_verify=False)
cc.login(username, password)
api = cc.api
ids = []

# collect all device ids
for result in api.dna.intent.api.v1("network-device").get(
    params={"managementIpAddress": ["100.75.1.11"]}
):
    ids.append(result["id"])


res = api.dna.intent.api.v1("network-device-archive").cleartext.post(
    body={"deviceId": ids, "password": zip_password}
)

# download task result

cc.download(res.get("url"), res.get("taskId") + ".zip")
