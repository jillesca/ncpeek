import pytest
from ncpeek.parsers.remove_namespaces import (
    remove_namespaces_from_dict,
)


DATA_TO_PARSE = {
    "data": {
        "@xmlns": "urn:ietf:params:xml:ns:netconf:base:1.0",
        "@xmlns:nc": "urn:ietf:params:xml:ns:netconf:base:1.0",
        "system-time": {
            "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-shellutil-oper",
            "clock": {
                "year": "2023",
                "month": "12",
                "day": "30",
                "hour": "16",
                "minute": "30",
                "second": "39",
                "millisecond": "768",
                "wday": "6",
                "time-zone": "UTC",
                "time-source": "ntp",
            },
            "uptime": {"host-name": "sandbox-iosxr", "uptime": "1568064"},
        },
        "interfaces": {
            "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-pfi-im-cmd-oper",
            "interfaces": {
                "interface": [
                    {"interface-name": "GigabitEthernet0/0/0/0"},
                    {"interface-name": "GigabitEthernet0/0/0/0.100"},
                    {"interface-name": "GigabitEthernet0/0/0/0.200"},
                    {"interface-name": "GigabitEthernet0/0/0/0.300"},
                    {"interface-name": "GigabitEthernet0/0/0/1"},
                    {"interface-name": "GigabitEthernet0/0/0/2"},
                    {"interface-name": "GigabitEthernet0/0/0/3"},
                    {"interface-name": "GigabitEthernet0/0/0/4"},
                    {"interface-name": "GigabitEthernet0/0/0/5"},
                    {"interface-name": "GigabitEthernet0/0/0/6"},
                    {"interface-name": "Loopback100"},
                    {"interface-name": "Loopback1001"},
                    {"interface-name": "Loopback103"},
                    {"interface-name": "Loopback1032"},
                    {"interface-name": "Loopback2"},
                    {"interface-name": "Loopback205"},
                    {"interface-name": "Loopback2222"},
                    {"interface-name": "Loopback24"},
                    {"interface-name": "Loopback3"},
                    {"interface-name": "Loopback33"},
                    {"interface-name": "Loopback330"},
                    {"interface-name": "Loopback35"},
                    {"interface-name": "Loopback555"},
                    {"interface-name": "Loopback88"},
                    {"interface-name": "MgmtEth0/RP0/CPU0/0"},
                    {"interface-name": "Null0"},
                ]
            },
        },
        "inventory": {
            "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-invmgr-oper",
            "entities": {
                "entity": {
                    "name": "Rack 0",
                    "attributes": {
                        "inv-basic-bag": {
                            "software-revision": "7.3.2",
                            "serial-number": "B550ED1D0D9",
                            "model-name": "R-IOSXRV9000-CC",
                        }
                    },
                }
            },
        },
    }
}

EXPECTED_DATA = {
    "data": {
        "system-time": {
            "clock": {
                "year": "2023",
                "month": "12",
                "day": "30",
                "hour": "16",
                "minute": "30",
                "second": "39",
                "millisecond": "768",
                "wday": "6",
                "time-zone": "UTC",
                "time-source": "ntp",
            },
            "uptime": {"host-name": "sandbox-iosxr", "uptime": "1568064"},
        },
        "interfaces": {
            "interfaces": {
                "interface": [
                    {"interface-name": "GigabitEthernet0/0/0/0"},
                    {"interface-name": "GigabitEthernet0/0/0/0.100"},
                    {"interface-name": "GigabitEthernet0/0/0/0.200"},
                    {"interface-name": "GigabitEthernet0/0/0/0.300"},
                    {"interface-name": "GigabitEthernet0/0/0/1"},
                    {"interface-name": "GigabitEthernet0/0/0/2"},
                    {"interface-name": "GigabitEthernet0/0/0/3"},
                    {"interface-name": "GigabitEthernet0/0/0/4"},
                    {"interface-name": "GigabitEthernet0/0/0/5"},
                    {"interface-name": "GigabitEthernet0/0/0/6"},
                    {"interface-name": "Loopback100"},
                    {"interface-name": "Loopback1001"},
                    {"interface-name": "Loopback103"},
                    {"interface-name": "Loopback1032"},
                    {"interface-name": "Loopback2"},
                    {"interface-name": "Loopback205"},
                    {"interface-name": "Loopback2222"},
                    {"interface-name": "Loopback24"},
                    {"interface-name": "Loopback3"},
                    {"interface-name": "Loopback33"},
                    {"interface-name": "Loopback330"},
                    {"interface-name": "Loopback35"},
                    {"interface-name": "Loopback555"},
                    {"interface-name": "Loopback88"},
                    {"interface-name": "MgmtEth0/RP0/CPU0/0"},
                    {"interface-name": "Null0"},
                ]
            },
        },
        "inventory": {
            "entities": {
                "entity": {
                    "name": "Rack 0",
                    "attributes": {
                        "inv-basic-bag": {
                            "software-revision": "7.3.2",
                            "serial-number": "B550ED1D0D9",
                            "model-name": "R-IOSXRV9000-CC",
                        }
                    },
                }
            },
        },
    }
}


def test_remove_namespaces_from_dict():
    """
    Test for default parser.
    """

    assert remove_namespaces_from_dict(DATA_TO_PARSE) == EXPECTED_DATA
