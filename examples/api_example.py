from ncpeek.client import NetconfClient


# XML_FILTER: str = """
# <filter>
#   <system xmlns="http://openconfig.net/yang/system">
#     <state>
#       <hostname />
#     </state>
#   </system>
# </filter>
# """

# XR_SETTINGS: list[dict] = [
#     {
#         "host": "sandbox-iosxr-1.cisco.com",
#         "port": 830,
#         "username": "admin",
#         "password": "C1sco12345",
#         "hostkey_verify": "False",
#         "timeout": 60,
#         "device_params": {"name": "iosxr"},
#         "allow_agent": "False",
#         "look_for_keys": "False",
#     }
# ]

device_settings = "cat8000v-0_settings.json"

XPATH_FILTER = "http://cisco.com/ns/yang/Cisco-IOS-XE-isis-oper:/isis-oper-data/isis-instance"


def api_call() -> None:
    """Example NetconfClient API"""
    client = NetconfClient()
    client.set_devices_settings(device_settings=device_settings)
    # client.set_xml_filter(xml_filter=XML_FILTER)
    client.set_xpath_filter(xpath_filter=XPATH_FILTER)
    try:
        result = client.fetch()
    except Exception as err:
        result = [{"error": f"{err=}"}]
    print(result)


if __name__ == "__main__":
    api_call()
