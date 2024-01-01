from typing import Optional
from dataclasses import dataclass


from ncpeek.utils.text_utils import (
    convert_json_to_dict,
    is_string_valid_xml,
)
from ncpeek.utils.file_utils import (
    read_file,
    resolve_filter_path,
    resolve_devices_path,
    remove_path_from_filename,
)
from ncpeek.args.arg_parser import create_argument_parser
from ncpeek.args.xpath_parse import extract_xpath


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
        return self._device_settings

    def get_filter_id(self) -> str:
        """Get the filter id."""
        return self._filter_id

    def get_netconf_filter(self) -> str:
        """Get the network filter."""
        return self._network_filter

    def _parse_xml_filter(self, filter_id: str) -> None:
        """Parse XML filter from a provided string."""
        if is_string_valid_xml(filter_id):
            self._filter_id = "generic"
            self._network_filter = filter_id
            return

        self._filter_id = remove_path_from_filename(filename=filter_id)
        network_filter = read_file(resolve_filter_path(filename=filter_id))
        if is_string_valid_xml(network_filter):
            self._network_filter = network_filter
        else:
            raise ValueError("No valid XML found in file/string")

    def _parse_xpath_filter(self, filter_id: str) -> None:
        """Parse XPath filter from a provided string."""
        self._filter_id = remove_path_from_filename(filename=filter_id)
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
                file_path = resolve_devices_path(filename=device_settings)
                return convert_json_to_dict(read_file(filename=file_path))
