from typing import List, Union
from dataclasses import dataclass
from ncpeek.utils.text_utils import (
    convert_xml_to_dict,
    convert_dict_to_json,
    convert_json_to_dict,
)
from ncpeek.netconf_devices import NetconfDevice
from ncpeek.args.parse_settings import SettingsParser
from ncpeek.factory.factory_parsers import get_parser
from ncpeek.netconf_session import NetconfSessionManager


@dataclass
class NetconfClient:
    """
    Main class for handling NetconfClient operations.
    """

    settings = SettingsParser()

    def execute_cli(self) -> str:
        """Executes command-line interface."""
        self.settings.parse_arguments()
        return self.run()

    def set_devices_settings(
        self, device_settings: [Union[list, str]]
    ) -> None:
        """
        API: sets devices settings directly.
        Can be a python list, a json string or a string
        with the name of the json file.
        See examples under ncpeek/devices
        """
        self.settings.set_device_settings(device_settings)

    def set_xml_filter(self, xml_filter: str) -> None:
        """
        API: sets XML filter directly.
        Can be the filename of a xml file (relative and absolute paths accepted)
        or can be a python string with valid xml.
        """
        self.settings.set_xml_filter(xml_filter)

    def set_xpath_filter(self, xpath_filter: str) -> None:
        """API: sets XPath filter directly."""
        self.settings.set_xpath_filter(xpath_filter)

    def run(self) -> str:
        """Runs the main operations and returns results in JSON format."""
        filter_id = self.settings.get_filter_id()
        net_filter = self.settings.get_network_filter()
        devices = self.settings.get_device_settings()
        results = self._get_data_from_devices(devices, net_filter, filter_id)
        return self._convert_results_to_json(results)

    def _get_data_from_devices(
        self, devices: list, net_filter: str, filter_id: str
    ) -> List[dict]:
        """Gets and parses data from devices."""
        results = []
        for device in devices:
            try:
                net_device = NetconfDevice(**device)
                session = NetconfSessionManager(net_device)
                rpc_reply = session.retrieve_data(net_filter)
                data_dict = convert_xml_to_dict(rpc_reply.data_xml)
                parser = get_parser(filter_id)
                data_parsed = parser.parse(data_dict, net_device, filter_id)
                results += data_parsed
            except Exception as err:
                results.append({"error": f"{err=}"})
        return results

    def _convert_results_to_json(self, data: list[dict]) -> str:
        result = convert_dict_to_json(data)
        assert convert_json_to_dict(result)
        return result


def ncpeek_cli() -> str:
    """Runs the netconf client using the CLI with the arguments supplied."""
    client = NetconfClient()
    print(client.execute_cli())


if __name__ == "__main__":
    ncpeek_cli()
