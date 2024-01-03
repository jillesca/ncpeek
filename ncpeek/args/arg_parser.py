import sys
import argparse
from argparse import RawTextHelpFormatter

NCPEEK_DESCRIPTION = """'ncpeek' is a netconf client designed to fetch data from various devices.
The client can be utilized in two distinct ways, 
either via Command Line Interface (CLI) or Application Programming Interface (API).
The data retrieval can be filtered through either XML or XPath, 
however, only one filter type can be applied at a given time.
Note that in CLI mode, only filenames can be treated as arguments.
Source code: https://github.com/jillesca/ncpeek"""

DEVICE_SETTINGS_DESCRIPTION = """Specify JSON filename containing device settings.
Visit https://github.com/jillesca/ncpeek/tree/main/ncpeek/devices for more information."""

XML_FILTER_DESCRIPTION = """Specify XML filename containing XML filter.
Visit https://github.com/jillesca/ncpeek/tree/main/ncpeek/filters for more details."""

XPATH_FILTER_DESCRIPTION = """Formats: <xpath> OR <namespace>:<xpath>
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
    parser = CustomArgumentParser(
        description=NCPEEK_DESCRIPTION, formatter_class=RawTextHelpFormatter
    )
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
