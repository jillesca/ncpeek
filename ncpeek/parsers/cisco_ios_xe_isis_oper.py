from typing import Optional
from dataclasses import dataclass, field
from ncpeek.netconf_parsers import Parser
from ncpeek.netconf_devices import NetconfDevice


@dataclass
class ISISStatsIOSXEParser(Parser):
    """
    A parser for ISIS stats for IOSXE devices.
    """

    device: NetconfDevice = None
    isis_interfaces_adj_up: int = 0
    stats: list = field(default_factory=list)
    netconf_filter_id: Optional[str] = None

    def parse(
        self,
        data_to_parse: dict,
        device: NetconfDevice,
        netconf_filter_id: str,
    ) -> list[dict]:
        """
        Parse ISIS stats data.

        Args:
            data (Dict): The data to parse.
            device (NetconfDevice): The device the data is related to.
            netconf_filter_id (str): The filter ID used for netconf.

        Returns:
            List[Dict]: The parsed data.
        """
        self.device = device
        self._extract_neighbor_stats(data=data_to_parse)
        self.netconf_filter_id = netconf_filter_id
        return self.stats

    def _extract_neighbor_stats(self, data: dict) -> None:
        isis_instances: dict = data["data"]["isis-oper-data"]["isis-instance"]

        for key, isis_instance in isis_instances.items():
            if "isis-neighbor" in key:
                self._count_adjcencies(instance=isis_instance)
                self._extract_metadata(instance=isis_instance)

    def _count_adjcencies(self, instance: list) -> None:
        """If you have 2 isis interfaces data comes inside a list.
        if you shutdown one interface and only 1 is up,
        the data will not come insdie a list."""
        if isinstance(instance, list):
            for neighbor in instance:
                if "isis-adj-up" in neighbor["state"]:
                    self.isis_interfaces_adj_up += 1
        else:
            if "isis-adj-up" in instance["state"]:
                self.isis_interfaces_adj_up += 1

    def _extract_metadata(self, instance: list) -> None:
        if isinstance(instance, list):
            for neighbor in instance:
                self.stats.append(
                    self._get_neighbor_metadata(neighbor=neighbor)
                )
        else:
            self.stats.append(self._get_neighbor_metadata(neighbor=instance))

    def _get_neighbor_metadata(self, neighbor: dict) -> dict:
        return {
            "isis_interfaces_adj_up": self.isis_interfaces_adj_up,
            "isis_status": neighbor["state"],
            "neighbor_id": neighbor["system-id"].replace(" ", "_"),
            "field": self.netconf_filter_id,
            "device": self.device.host,
            "ip": self.device.host,
            "interface_name": neighbor["if-name"],
            "ipv4_address": neighbor["ipv4-address"],
        }
