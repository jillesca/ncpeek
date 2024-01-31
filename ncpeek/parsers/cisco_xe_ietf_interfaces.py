from typing import Optional
from dataclasses import dataclass
from ncpeek.netconf_parsers import Parser
from ncpeek.netconf_devices import NetconfDevice


@dataclass
class InterfaceStatsIETF_IOSXEParser(Parser):
    """
    A parser for interface stats for IETF IOSXE devices.
    """

    device: NetconfDevice = None
    netconf_filter_id: Optional[str] = None

    def parse(
        self,
        data_to_parse: dict,
        device: NetconfDevice,
        netconf_filter_id: str,
    ) -> list[dict]:
        """
        Parse interface stats data.

        Args:
            data (Dict): The data to parse.
            device (NetconfDevice): The device the data is related to.
            netconf_filter_id (str): The filter ID used for netconf.

        Returns:
            List[Dict]: The parsed data.
        """
        self.device = device
        self.netconf_filter_id = netconf_filter_id
        return self._extract_interface_stats(data=data_to_parse)

    def _extract_interface_stats(self, data: dict) -> list[dict]:
        stats: list = []
        interfaces: dict = data["data"]["interfaces-state"]["interface"]

        for interface in interfaces:
            stats.append(self._get_interface_stats(interface=interface))
        return stats

    def _get_interface_stats(self, interface: dict) -> dict:
        return {
            "operational_status": 1 if interface["oper-status"] == "up" else 0,
            "in_octets": int(interface["statistics"]["in-octets"]),
            "in_errors": int(interface["statistics"]["in-errors"]),
            "out_octets": int(interface["statistics"]["out-octets"]),
            "out_errors": int(interface["statistics"]["out-errors"]),
            "name": interface["name"].replace(" ", "_"),
            "field": self.netconf_filter_id,
            "device": self.device.hostname,
            "ip": self.device.host,
        }
