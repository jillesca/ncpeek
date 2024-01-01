import pytest
from ncpeek.args.parse_settings import SettingsParser


def test_set_device_settings():
    """
    Test setting device settings from a json file.
    """
    test_device_settings_file = "devnet_xr_sandbox.json"
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
    parser = SettingsParser()
    parser.set_device_settings(test_device_settings_file)

    assert parser.get_device_settings() == device_settings_file_result


def test_set_device_settings_as_dict():
    """
    Test setting device settings directly as a dictionary.
    """

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
    parser = SettingsParser()
    parser.set_device_settings(device_settings_file_result)

    assert parser.get_device_settings() == device_settings_file_result


def test_set_xml_filter():
    """
    Test setting XML filter from a provided string.
    """
    test_xml_filter_file = "Cisco-IOS-XR-hostname.xml"

    network_filter_result = '<filter>\n  <system xmlns="http://openconfig.net/yang/system">\n    <state>\n      <hostname />\n    </state>\n  </system>\n</filter>'

    parser = SettingsParser()
    parser.set_xml_filter(test_xml_filter_file)

    assert parser.get_filter_id() == test_xml_filter_file
    assert parser.get_network_filter() == network_filter_result


def test_set_xml_filter_as_string():
    """
    Test setting XML filter from a provided string.
    """
    test_xml_filter_string = """<filter>
  <system xmlns="http://openconfig.net/yang/system">
    <state>
      <hostname />
    </state>
  </system>
</filter>"""

    parser = SettingsParser()
    parser.set_xml_filter(test_xml_filter_string)

    assert parser.get_filter_id() == "generic"
    assert parser.get_network_filter() == test_xml_filter_string


def test_set_xpath_filter():
    """
    Test setting XPath filter from a provided string.
    """
    test_xpath_filter = (
        "http://cisco.com/ns/yang/Cisco-IOS-XE-native:/native/hostname"
    )
    xpath_filter_result = (
        "xpath",
        (
            {"ns0": "http://cisco.com/ns/yang/Cisco-IOS-XE-native"},
            "/native/hostname",
        ),
    )

    parser = SettingsParser()
    parser.set_xpath_filter(test_xpath_filter)

    assert parser.get_filter_id() == test_xpath_filter
    assert parser.get_network_filter() == xpath_filter_result
