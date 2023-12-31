import pytest
from ncpeek.client import NetconfClient


@pytest.fixture
def client():
    """Return a new instance of the NetconfClient class."""
    return NetconfClient()


def test_set_devices_settings(client):
    """
    Test setting devices settings directly.
    """
    test_device_settings_file = "devnet_xr_sandbox_settings.json"
    device_settings_file_result = [
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
    client.set_devices_settings(test_device_settings_file)
    assert client.settings.get_device_settings() == device_settings_file_result


def test_set_xml_filter(client):
    """
    Test setting XML filter directly.
    """
    test_xml_filter_file = "Cisco-IOS-XR-hostname.xml"

    client.set_xml_filter(test_xml_filter_file)
    assert client.settings.get_filter_id() == test_xml_filter_file


def test_set_xpath_filter(client):
    """
    Test setting XPath filter directly.
    """
    test_xpath_filter = (
        "http://cisco.com/ns/yang/Cisco-IOS-XE-native:/native/hostname"
    )
    client.set_xpath_filter(test_xpath_filter)
    assert client.settings.get_filter_id() == test_xpath_filter
