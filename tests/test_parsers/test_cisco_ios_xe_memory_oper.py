import pytest
from ncpeek.parsers.cisco_ios_xe_memory_oper import (
    CiscoIOSXEMemoryParser,
)
from ncpeek.netconf_devices import NetconfDevice

NETCONF_FILTER_ID = "Cisco-IOS-XE-memory-oper.xml"

DATA_TO_PARSE = {
    "data": {
        "@xmlns": "urn:ietf:params:xml:ns:netconf:base:1.0",
        "@xmlns:nc": "urn:ietf:params:xml:ns:netconf:base:1.0",
        "memory-statistics": {
            "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper",
            "memory-statistic": [
                {
                    "name": "Processor",
                    "total-memory": "2028113884",
                    "used-memory": "192040880",
                },
                {
                    "name": "reserve Processor",
                    "total-memory": "102404",
                    "used-memory": "92",
                },
                {
                    "name": "lsmpi_io",
                    "total-memory": "3149400",
                    "used-memory": "3148576",
                },
            ],
        },
    }
}

EXPECTED_DATA = [
    {
        "name": "Processor",
        "percent_used": 9.468939664336915,
        "field": "Cisco-IOS-XE-memory-oper.xml",
        "device": "localhost",
        "ip": "localhost",
    },
    {
        "name": "reserve Processor",
        "percent_used": 0.08984024061560095,
        "field": "Cisco-IOS-XE-memory-oper.xml",
        "device": "localhost",
        "ip": "localhost",
    },
    {
        "name": "lsmpi_io",
        "percent_used": 99.97383628627675,
        "field": "Cisco-IOS-XE-memory-oper.xml",
        "device": "localhost",
        "ip": "localhost",
    },
]


def test_CiscoIOSXEMemoryParser_parser():
    """
    Test for CiscoIOSXEMemoryParser
    """

    test_parser = CiscoIOSXEMemoryParser()
    result = test_parser.parse(
        data_to_parse=DATA_TO_PARSE,
        device=NetconfDevice(
            host="localhost", username="user", password="pass"
        ),
        netconf_filter_id=NETCONF_FILTER_ID,
    )

    assert result == EXPECTED_DATA
