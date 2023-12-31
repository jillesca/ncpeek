from typing import Dict

PARSER_MAPPING: Dict[str, Dict[str, str]] = {
    "default_parser": {
        "module": "ncpeek.parsers.default_parser",
        "class": "DefaultParser",
    },
    "cisco_xe_ietf-interfaces.xml": {
        "module": "ncpeek.parsers.cisco_xe_ietf_interfaces",
        "class": "InterfaceStatsIETF_IOSXEParser",
    },
    "Cisco-IOS-XE-interfaces-oper.xml": {
        "module": "ncpeek.parsers.cisco_ios_xe_interfaces_oper",
        "class": "InterfaceStatsIOSXEParser",
    },
    "Cisco-IOS-XE-memory-oper.xml": {
        "module": "ncpeek.parsers.cisco_ios_xe_memory_oper",
        "class": "CiscoIOSXEMemoryParser",
    },
    "http://cisco.com/ns/yang/Cisco-IOS-XE-isis-oper:/isis-oper-data/isis-instance": {
        "module": "ncpeek.parsers.cisco_ios_xe_isis_oper",
        "class": "ISISStatsIOSXEParser",
    },
}
