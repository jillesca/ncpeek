from typing import Optional
from dataclasses import dataclass
from ncpeek.netconf_parsers import Parser
from ncpeek.netconf_devices import NetconfDevice


def _calculate_percentage(entry: dict) -> int:
    return (int(entry["used-memory"]) / int(entry["total-memory"])) * 100


@dataclass
class CiscoIOSXEMemoryParser(Parser):
    """
    A parser for memory data for Cisco IOSXE devices.
    """

    netconf_filter_id: Optional[str] = None
    device: Optional[NetconfDevice] = None

    def parse(
        self,
        data_to_parse: dict,
        device: NetconfDevice,
        netconf_filter_id: str,
    ) -> list[dict]:
        """
        Parse memory data.

        Args:
            data_to_parse (Dict): The data to parse.
            net_device (NetconfDevice): The device the data is related to.
            netconf_filter_id (str): The filter ID used for netconf.

        Returns:
            List[Dict]: The parsed data.
        """
        self.device = device
        self.netconf_filter_id = netconf_filter_id
        return self._extract_memory_statistics(rpc_reply=data_to_parse)

    def _extract_memory_statistics(self, rpc_reply: dict) -> str:
        stats: list = []
        xpath: dict = rpc_reply["data"]["memory-statistics"][
            "memory-statistic"
        ]

        for entry in xpath:
            stats.append(self._get_memory_stats(entry=entry))
        return stats

    def _get_memory_stats(self, entry: dict) -> dict:
        return {
            "name": entry["name"],
            "percent_used": _calculate_percentage(entry),
            "field": self.netconf_filter_id,
            "device": self.device.hostname,
            "ip": self.device.host,
        }
