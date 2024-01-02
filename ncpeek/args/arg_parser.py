import sys
import argparse

NCPEEK_DESCRIPTION = """Netconf client to gather data from devices.
    The client can be used via CLI or API.
    Provide device credentials and options via a json file.
    User must specify if an XML filter or XPath is to be used.
    Note that only one can be used."""

DEVICE_SETTINGS_DESCRIPTION = """Device Settings in json format.
    See examples under ncpeek/devices"""

XML_FILTER_DESCRIPTION = """Netconf Filter to apply in XML format.
    See examples under ncpeek/filters"""

XPATH_FILTER_DESCRIPTION = """Netconf Filter to apply in XPath. 
    Formats: <xpath> OR <namespace>:<xpath>
    Example: 'interfaces/interface' OR 
    'http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper:interfaces/interface'"""


class CustomArgumentParser(argparse.ArgumentParser):
    """
    Custom ArgumentParser class to display help message on error.
    """

    def error(self, message: str) -> None:
        sys.stderr.write(f"Error: {message}")
        self.print_help()
        sys.exit(2)


def create_argument_parser():
    """
    Create and return an argument parser with mutually exclusive arguments.
    For device settings and filter options.
    """
    parser = CustomArgumentParser(description=NCPEEK_DESCRIPTION)
    group = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument(
        "-d",
        "--device-settings",
        help=DEVICE_SETTINGS_DESCRIPTION,
    )

    group.add_argument(
        "-x",
        "--xml-filter",
        help=XML_FILTER_DESCRIPTION,
    )

    group.add_argument(
        "-p",
        "--xpath-filter",
        help=XPATH_FILTER_DESCRIPTION,
    )

    return parser
