import pytest
from ncpeek.parsers.cisco_ios_xe_isis_oper import ISISStatsIOSXEParser
from ncpeek.netconf_devices import NetconfDevice

device = NetconfDevice(
    hostname="device-1",
    host="192.168.1.1",
    password="password",
    username="username",
)
parser = ISISStatsIOSXEParser(device=device)
filter_id = "filter1"

data_to_parse = {
    "data": {
        "isis-oper-data": {
            "isis-instance": {
                "isis-neighbor": [
                    {
                        "system-id": "00:00:00:00:00:0a",
                        "if-name": "GigabitEthernet1",
                        "level": "level-1",
                        "ipv4-address": "192.168.0.1",
                        "state": "isis-adj-up",
                        "holdtime": 60,
                    },
                    {
                        "system-id": "00:00:00:00:00:0a",
                        "if-name": "GigabitEthernet2",
                        "level": "level-2",
                        "ipv4-address": "192.168.0.2",
                        "state": "isis-adj-down",
                        "holdtime": 30,
                    },
                    {
                        "system-id": "00:00:00:00:00:0c",
                        "if-name": "GigabitEthernet2",
                        "level": "level-1",
                        "ipv4-address": "192.168.0.3",
                        "state": "isis-adj-up",
                        "holdtime": 45,
                    },
                ]
            }
        }
    }
}


def test_parse():
    parsed_data = parser.parse(data_to_parse, device, filter_id)
    expected_data = [
        {
            "device": "device-1",
            "field": "filter1",
            "ip": "192.168.1.1",
            "isis-neighbors": [
                {
                    "local_interfaces_status": [
                        {
                            "holdtime": 60,
                            "interface_name": "GigabitEthernet1",
                            "isis_status": "isis-adj-up",
                            "level": "level-1",
                            "local_ipv4_address": "192.168.0.1",
                        },
                        {
                            "holdtime": 30,
                            "interface_name": "GigabitEthernet2",
                            "isis_status": "isis-adj-down",
                            "level": "level-2",
                            "local_ipv4_address": "192.168.0.2",
                        },
                    ],
                    "neighbor_status": 1,
                    "system-id": "00:00:00:00:00:0a",
                },
                {
                    "local_interfaces_status": [
                        {
                            "holdtime": 45,
                            "interface_name": "GigabitEthernet2",
                            "isis_status": "isis-adj-up",
                            "level": "level-1",
                            "local_ipv4_address": "192.168.0.3",
                        }
                    ],
                    "neighbor_status": 1,
                    "system-id": "00:00:00:00:00:0c",
                },
            ],
            "isis_neighbors_count": 2,
        }
    ]
    assert parsed_data == expected_data


def test_group_data_by_system_id():
    grouped_data = parser._group_data_by_system_id(data_to_parse)
    expected_data = {
        "00:00:00:00:00:0a": [
            {
                "holdtime": 60,
                "interface_name": "GigabitEthernet1",
                "isis_status": "isis-adj-up",
                "level": "level-1",
                "local_ipv4_address": "192.168.0.1",
            },
            {
                "holdtime": 30,
                "interface_name": "GigabitEthernet2",
                "isis_status": "isis-adj-down",
                "level": "level-2",
                "local_ipv4_address": "192.168.0.2",
            },
        ],
        "00:00:00:00:00:0c": [
            {
                "holdtime": 45,
                "interface_name": "GigabitEthernet2",
                "isis_status": "isis-adj-up",
                "level": "level-1",
                "local_ipv4_address": "192.168.0.3",
            }
        ],
    }

    assert grouped_data == expected_data
