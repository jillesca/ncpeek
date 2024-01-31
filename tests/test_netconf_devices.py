import pytest
from ncpeek.netconf_devices import NetconfDevice


def test_NetconfDevice_init():
    # Test normal initialization
    device = NetconfDevice(host="localhost", username="user", password="pass")
    assert device.host == "localhost"
    assert device.username == "user"
    assert device.password == "pass"

    # Test default values
    assert device.port == 830
    assert device.timeout == 60
    assert device.hostkey_verify is False
    assert device.allow_agent is True
    assert device.look_for_keys is True


def test_NetconfDevice_missing_fields():
    # Test missing host
    with pytest.raises(ValueError):
        NetconfDevice(username="user", password="pass")

    # Test missing username
    with pytest.raises(ValueError):
        NetconfDevice(host="localhost", password="pass")

    # Test missing password
    with pytest.raises(ValueError):
        NetconfDevice(host="localhost", username="user")


def test_NetconfDevice_parse_boolean():
    # Test string to boolean conversion
    device = NetconfDevice(
        host="localhost",
        username="user",
        password="pass",
        hostkey_verify="true",
        allow_agent="false",
        look_for_keys="false",
    )
    assert device.hostkey_verify is True
    assert device.allow_agent is False
    assert device.look_for_keys is False

    # Test invalid boolean
    with pytest.raises(ValueError):
        NetconfDevice(
            host="localhost",
            username="user",
            password="pass",
            hostkey_verify="not_a_boolean",
        )


def test_NetconfDevice_set_hostname():
    # Test when hostname is not set
    device = NetconfDevice(host="localhost", username="user", password="pass")
    device._set_hostname()
    assert device.hostname == "localhost"

    # Test when hostname is already set
    device = NetconfDevice(
        host="localhost",
        username="user",
        password="pass",
        hostname="example.com",
    )
    device._set_hostname()
    assert device.hostname == "example.com"
