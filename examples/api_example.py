from ncpeek.client import NetconfClient

xml_filter: str = """
<filter>
  <system xmlns="http://openconfig.net/yang/system">
    <state>
      <hostname />
    </state>
  </system>
</filter>
"""

xr_device_settings: dict = [
    {
        "host": "sandbox-iosxr-1.cisco.com",
        "port": 830,
        "username": "admin",
        "password": "C1sco12345",
        "hostkey_verify": "False",
        "timeout": 60,
        "device_params": {"name": "iosxr"},
        "allow_agent": "False",
        "look_for_keys": "False",
    }
]


def api_call() -> None:
    """Example NetconfClient API"""
    client = NetconfClient()
    client.set_devices_settings(xr_device_settings)
    client.set_xml_filter(xml_filter)
    try:
        result = client.fetch()
    except Exception as err:
        result = [{"error": f"{err=}"}]
    print(result)


if __name__ == "__main__":
    api_call()
