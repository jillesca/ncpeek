import pytest
from ncpeek.parsers.cisco_xe_ietf_interfaces import (
    InterfaceStatsIETF_IOSXEParser,
)
from ncpeek.netconf_devices import NetconfDevice


NETCONF_FILTER_ID = "cisco_xe_ietf-interfaces.xml"

EXPECTED_DATA = [
    {
        "operational_status": 1,
        "in_octets": 3435605,
        "in_errors": 0,
        "out_octets": 35813498,
        "out_errors": 0,
        "name": "GigabitEthernet1",
        "field": "cisco_xe_ietf-interfaces.xml",
        "device": "localhost",
        "ip": "localhost",
    },
    {
        "operational_status": 1,
        "in_octets": 0,
        "in_errors": 0,
        "out_octets": 22776,
        "out_errors": 0,
        "name": "Loopback0",
        "field": "cisco_xe_ietf-interfaces.xml",
        "device": "localhost",
        "ip": "localhost",
    },
]

DATA_TO_PARSE = {
    "data": {
        "@xmlns": "urn:ietf:params:xml:ns:netconf:base:1.0",
        "@xmlns:nc": "urn:ietf:params:xml:ns:netconf:base:1.0",
        "interfaces-state": {
            "@xmlns": "urn:ietf:params:xml:ns:yang:ietf-interfaces",
            "interface": [
                {
                    "name": "GigabitEthernet1",
                    "type": {
                        "@xmlns:ianaift": "urn:ietf:params:xml:ns:yang:iana-if-type",
                        "#text": "ianaift:ethernetCsmacd",
                    },
                    "oper-status": "up",
                    "statistics": {
                        "in-octets": "3435605",
                        "in-errors": "0",
                        "out-octets": "35813498",
                        "out-errors": "0",
                    },
                },
                {
                    "name": "Loopback0",
                    "type": {
                        "@xmlns:ianaift": "urn:ietf:params:xml:ns:yang:iana-if-type",
                        "#text": "ianaift:softwareLoopback",
                    },
                    "oper-status": "up",
                    "statistics": {
                        "in-octets": "0",
                        "in-errors": "0",
                        "out-octets": "22776",
                        "out-errors": "0",
                    },
                },
            ],
        },
    }
}


def test_InterfaceStatsIETF_IOSXEParser_parser():
    """
    Test for InterfaceStatsIETF_IOSXEParser
    """

    test_parser = InterfaceStatsIETF_IOSXEParser()
    result = test_parser.parse(
        data_to_parse=DATA_TO_PARSE,
        device=NetconfDevice(
            host="localhost", username="user", password="pass"
        ),
        netconf_filter_id=NETCONF_FILTER_ID,
    )

    assert result == EXPECTED_DATA
