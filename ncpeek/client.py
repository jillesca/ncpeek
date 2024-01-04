from typing import Optional, Union
from dataclasses import dataclass
from ncpeek.utils.text_utils import (
    convert_xml_to_dict,
    convert_dict_to_json,
)
from ncpeek.netconf_devices import NetconfDevice
from ncpeek.args.parse_settings import SettingsParser
from ncpeek.factory.factory_parsers import get_parser
from ncpeek.netconf_session import NetconfSession

DEFAULT_NETCONF_OPERATION = "fetch"


@dataclass
class NetconfClient:
    """
    Main class for handling NetconfClient operations.
    """

    _settings = SettingsParser()
    _operation: Optional[str] = DEFAULT_NETCONF_OPERATION
    _filter_id: Optional[str] = None
    _netconf_filter: Optional[str] = None

    def execute_cli(self) -> str:
        """Executes command-line interface."""
        self._settings.parse_arguments()
        return self._run()

    def set_devices_settings(self, device_settings: Union[list, str]) -> None:
        """
        API: sets devices settings directly.
        Can be a python list, a json string or a string
        with the name of the json file.
        See examples under ncpeek/devices
        """
        self._settings.set_device_settings(device_settings)

    def set_xml_filter(self, xml_filter: str) -> None:
        """
        API: sets XML filter directly.
        Can be the filename of a xml file (relative and absolute paths accepted)
        or can be a python string with valid xml.
        """
        self._settings.set_xml_filter(xml_filter)

    def set_xpath_filter(self, xpath_filter: str) -> None:
        """API: sets XPath filter directly."""
        self._settings.set_xpath_filter(xpath_filter)

    def fetch(self) -> str:
        """Fetchs data from network device

        Returns:
            str: rpc reply from network device
        """
        self._operation = "fetch"
        return self._run()

    def _run(self) -> str:
        """Runs the main operations and returns results in JSON format."""

        devices = self._settings.get_device_settings()
        self._filter_id = self._settings.get_filter_id()
        self._netconf_filter = self._settings.get_netconf_filter()

        results = []
        for device in devices:
            results += self._process_device(device)

        return convert_dict_to_json(results)

    def _process_device(self, device: dict) -> dict:
        """Processes a single device operation and parsing its reply."""
        try:
            device = NetconfDevice(**device)
            rpc = NetconfSession(
                device=device,
                netconf_filter=self._netconf_filter,
                operation=self._operation,
            )
            data_dict = convert_xml_to_dict(xml_string=rpc.reply())
            parser = get_parser(netconf_filter=self._filter_id)
            parsed_data = parser.parse(
                data_to_parse=data_dict,
                device=device,
                netconf_filter_id=self._filter_id,
            )
        except Exception as err:
            parsed_data = [{"error": f"{err=}"}]
        return parsed_data


def cli() -> None:
    """Runs the netconf client using the CLI with the arguments supplied."""
    client = NetconfClient()
    try:
        print(client.execute_cli())
    except Exception as err:
        print(f"Error found: {err=}")


if __name__ == "__main__":
    cli()
