import pytest
from ncpeek.parsers.cisco_ios_xe_interfaces_oper import (
    InterfaceStatsIOSXEParser,
)
from ncpeek.netconf_devices import NetconfDevice

NETCONF_FILTER_ID = "Cisco-IOS-XE-interfaces-oper.xml"

DATA_TO_PARSE = {
    "data": {
        "@xmlns": "urn:ietf:params:xml:ns:netconf:base:1.0",
        "@xmlns:nc": "urn:ietf:params:xml:ns:netconf:base:1.0",
        "interfaces": {
            "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper",
            "interface": [
                {
                    "name": "GigabitEthernet1",
                    "interface-type": "iana-iftype-ethernet-csmacd",
                    "admin-status": "if-state-up",
                    "oper-status": "if-oper-state-ready",
                    "statistics": {
                        "discontinuity-time": "2023-12-30T07:11:53+00:00",
                        "in-octets": "4249319",
                        "in-unicast-pkts": "40657",
                        "in-broadcast-pkts": "0",
                        "in-multicast-pkts": "0",
                        "in-discards": "0",
                        "in-errors": "0",
                        "in-unknown-protos": "0",
                        "out-octets": "43109295",
                        "out-unicast-pkts": "59250",
                        "out-broadcast-pkts": "0",
                        "out-multicast-pkts": "0",
                        "out-discards": "0",
                        "out-errors": "0",
                        "rx-pps": "3",
                        "rx-kbps": "3",
                        "tx-pps": "3",
                        "tx-kbps": "6",
                        "num-flaps": "0",
                        "in-crc-errors": "0",
                        "in-discards-64": "0",
                        "in-errors-64": "0",
                        "in-unknown-protos-64": "0",
                        "out-octets-64": "43109295",
                    },
                },
                {
                    "name": "Loopback0",
                    "interface-type": "iana-iftype-sw-loopback",
                    "admin-status": "if-state-up",
                    "oper-status": "if-oper-state-ready",
                    "statistics": {
                        "discontinuity-time": "2023-12-30T07:11:53+00:00",
                        "in-octets": "0",
                        "in-unicast-pkts": "0",
                        "in-broadcast-pkts": "0",
                        "in-multicast-pkts": "0",
                        "in-discards": "0",
                        "in-errors": "0",
                        "in-unknown-protos": "0",
                        "out-octets": "24744",
                        "out-unicast-pkts": "312",
                        "out-broadcast-pkts": "0",
                        "out-multicast-pkts": "0",
                        "out-discards": "0",
                        "out-errors": "0",
                        "rx-pps": "0",
                        "rx-kbps": "0",
                        "tx-pps": "0",
                        "tx-kbps": "0",
                        "num-flaps": "0",
                        "in-crc-errors": "0",
                        "in-discards-64": "0",
                        "in-errors-64": "0",
                        "in-unknown-protos-64": "0",
                        "out-octets-64": "24744",
                    },
                },
            ],
        },
    }
}

EXPECTED_DATA = [
    {
        "in_octets": 4249319,
        "in_errors": 0,
        "out_octets": 43109295,
        "out_errors": 0,
        "in-broadcast-pkts": 0,
        "in-crc-errors": 0,
        "in-discards": 0,
        "in-discards-64": 0,
        "in-errors-64": 0,
        "in-multicast-pkts": 0,
        "in-unicast-pkts": 40657,
        "in-unknown-protos": 0,
        "in-unknown-protos-64": 0,
        "num-flaps": 0,
        "out-broadcast-pkts": 0,
        "out-discards": 0,
        "out-multicast-pkts": 0,
        "out-octets-64": 43109295,
        "out-unicast-pkts": 59250,
        "rx-kbps": 3,
        "rx-pps": 3,
        "tx-kbps": 6,
        "tx-pps": 3,
        "operational_status": 1,
        "name": "GigabitEthernet1",
        "field": "Cisco-IOS-XE-interfaces-oper.xml",
        "device": "localhost",
        "ip": "localhost",
    },
    {
        "in_octets": 0,
        "in_errors": 0,
        "out_octets": 24744,
        "out_errors": 0,
        "in-broadcast-pkts": 0,
        "in-crc-errors": 0,
        "in-discards": 0,
        "in-discards-64": 0,
        "in-errors-64": 0,
        "in-multicast-pkts": 0,
        "in-unicast-pkts": 0,
        "in-unknown-protos": 0,
        "in-unknown-protos-64": 0,
        "num-flaps": 0,
        "out-broadcast-pkts": 0,
        "out-discards": 0,
        "out-multicast-pkts": 0,
        "out-octets-64": 24744,
        "out-unicast-pkts": 312,
        "rx-kbps": 0,
        "rx-pps": 0,
        "tx-kbps": 0,
        "tx-pps": 0,
        "operational_status": 1,
        "name": "Loopback0",
        "field": "Cisco-IOS-XE-interfaces-oper.xml",
        "device": "localhost",
        "ip": "localhost",
    },
]


def test_InterfaceStatsIOSXEParser_parser():
    """
    Test for InterfaceStatsIOSXEParser
    """

    test_parser = InterfaceStatsIOSXEParser()
    result = test_parser.parse(
        data_to_parse=DATA_TO_PARSE,
        device=NetconfDevice(
            host="localhost", username="user", password="pass"
        ),
        netconf_filter_id=NETCONF_FILTER_ID,
    )

    assert result == EXPECTED_DATA
