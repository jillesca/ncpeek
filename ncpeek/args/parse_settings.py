from typing import Optional
from dataclasses import dataclass
from ncpeek.utils.file_utils import (
    read_filter,
    read_settings,
    remove_path_from_filename,
)
from ncpeek.utils.text_utils import (
    is_string_valid_xml,
    convert_json_to_dict,
)
from ncpeek.args.xpath_parse import extract_xpath
from ncpeek.args.arg_parser import create_argument_parser


@dataclass
class SettingsParser:
    """
    A class to parse and handle settings for netconf client.
    """

    _filter_id: Optional[str] = None
    _network_filter: Optional[str] = None
    _device_settings: Optional[str] = None

    def parse_arguments(self) -> None:
        """Parse command-line arguments and set device settings and filters."""
        args = create_argument_parser().parse_args()
        self._device_settings = self._load_settings(args.device_settings)

        if args.xml_filter:
            self._parse_xml_filter(args.xml_filter)
        elif args.xpath_filter:
            self._parse_xpath_filter(args.xpath_filter)

    def set_device_settings(self, device_settings: str) -> None:
        """Set device settings from a json file."""
        self._device_settings = self._load_settings(device_settings)

    def set_xml_filter(self, xml_filter: str) -> None:
        """Set XML filter from a provided string."""
        self._parse_xml_filter(xml_filter)

    def set_xpath_filter(self, xpath_filter: str) -> None:
        """Set XPath filter from a provided string."""
        self._parse_xpath_filter(xpath_filter)

    def get_device_settings(self) -> str:
        """Get the device settings."""
        if not self._device_settings:
            raise ValueError("Device Settings not provided")
        return self._device_settings

    def get_filter_id(self) -> str:
        """Get the filter id."""
        if not self._filter_id:
            raise ValueError("filter not provided")
        return self._filter_id

    def get_netconf_filter(self) -> str:
        """Get the network filter."""
        return self._network_filter

    def _parse_xml_filter(self, filter_id: str) -> None:
        """Parse XML filter from a provided string."""
        if is_string_valid_xml(xml_string=filter_id):
            self._filter_id = "generic"
            self._network_filter = filter_id
            return

        try:
            self._set_filter_id(filter_id=filter_id)
            network_filter = read_filter(filename=filter_id)
        except Exception as err:
            raise ValueError(
                f"Error opening file {err=}. Make sure a valid filename is provided for a xml filter."
            ) from err
        if is_string_valid_xml(xml_string=network_filter):
            self._network_filter = network_filter
        else:
            raise ValueError("No valid XML found in file/string")

    def _parse_xpath_filter(self, filter_id: str) -> None:
        """Parse XPath filter from a provided string."""
        self._set_filter_id(filter_id=filter_id)
        self._network_filter = extract_xpath(netconf_filter=filter_id)

    def _load_settings(self, device_settings: str) -> dict:
        """Load settings from a provided string."""
        if isinstance(device_settings, list):
            return device_settings
        if isinstance(device_settings, str):
            try:
                # passing json directly
                return convert_json_to_dict(json_string=device_settings)
            except Exception:
                return convert_json_to_dict(
                    read_settings(filename=device_settings)
                )

    def _set_filter_id(self, filter_id: str) -> str:
        self._filter_id = remove_path_from_filename(filename=filter_id)
