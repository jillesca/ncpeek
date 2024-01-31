from typing import Optional
from collections import ChainMap
from dataclasses import dataclass
from ncpeek.netconf_parsers import Parser
from ncpeek.netconf_devices import NetconfDevice


@dataclass
class InterfaceStatsIOSXEParser(Parser):
    """A parser for interface stats for IOSXE devices."""

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
        return self._interface_stats(data=data_to_parse)

    def _interface_stats(self, data: dict) -> list[dict]:
        stats: list = []
        interfaces: dict = data["data"]["interfaces"]["interface"]

        for interface in interfaces:
            metadata = self._extract_metadata(interface=interface)
            intf_stats = self._extract_statistics(
                interface=interface["statistics"]
            )
            stats.append(dict(ChainMap(metadata, intf_stats)))
        return stats

    def _extract_metadata(self, interface: dict) -> dict:
        return {
            "operational_status": 1
            if interface["oper-status"] == "if-oper-state-ready"
            else 0,
            "name": interface["name"].replace(" ", "_"),
            "field": self.netconf_filter_id,
            "device": self.device.hostname,
            "ip": self.device.host,
        }

    def _extract_statistics(self, interface: dict) -> dict:
        return {
            "in_octets": int(interface["in-octets"]),
            "in_errors": int(interface["in-errors"]),
            "out_octets": int(interface["out-octets"]),
            "out_errors": int(interface["out-errors"]),
            "in-broadcast-pkts": int(interface["in-broadcast-pkts"]),
            "in-crc-errors": int(interface["in-crc-errors"]),
            "in-discards": int(interface["in-discards"]),
            "in-discards-64": int(interface["in-discards-64"]),
            "in-errors-64": int(interface["in-errors-64"]),
            "in-multicast-pkts": int(interface["in-multicast-pkts"]),
            "in-unicast-pkts": int(interface["in-unicast-pkts"]),
            "in-unknown-protos": int(interface["in-unknown-protos"]),
            "in-unknown-protos-64": int(interface["in-unknown-protos-64"]),
            "num-flaps": int(interface["num-flaps"]),
            "out-broadcast-pkts": int(interface["out-broadcast-pkts"]),
            "out-discards": int(interface["out-discards"]),
            "out-multicast-pkts": int(interface["out-multicast-pkts"]),
            "out-octets-64": int(interface["out-octets-64"]),
            "out-unicast-pkts": int(interface["out-unicast-pkts"]),
            "rx-kbps": int(interface["rx-kbps"]),
            "rx-pps": int(interface["rx-pps"]),
            "tx-kbps": int(interface["tx-kbps"]),
            "tx-pps": int(interface["tx-pps"]),
        }
