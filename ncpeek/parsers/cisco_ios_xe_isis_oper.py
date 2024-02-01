from collections import defaultdict
from typing import List, Dict
from ncpeek.netconf_parsers import Parser
from ncpeek.netconf_devices import NetconfDevice


class ISISStatsIOSXEParser(Parser):
    """
    A parser for ISIS stats for IOSXE devices.
    """

    def __init__(self, device: NetconfDevice = None):
        """
        Initialize the parser.

        Args:
            device (NetconfDevice, optional): The device to parse data for. Defaults to None.
        """
        self.device = device
        self.parsed_stats = []

    def parse(
        self,
        data_to_parse: Dict,
        device: NetconfDevice,
        netconf_filter_id: str,
    ) -> List[Dict]:
        """
        Parse ISIS stats data.

        Args:
            data (Dict): The data to parse.
            device (NetconfDevice): The device the data is related to.
            filter_id (str): The filter ID used for netconf.

        Returns:
            List[Dict]: The parsed data.
        """
        self.device = device
        self.filter_id = netconf_filter_id
        grouped_data = self._group_data_by_system_id(data_to_parse)
        return self._prepare_output_data(grouped_data)

    def _group_data_by_system_id(self, data: Dict) -> Dict:
        """
        Group data by system-id.

        Args:
            data (Dict): The data to group.

        Returns:
            Dict: The grouped data.
        """
        grouped_data = defaultdict(list)
        for neighbor in data["data"]["isis-oper-data"]["isis-instance"][
            "isis-neighbor"
        ]:
            grouped_data[neighbor["system-id"]].append(
                self._create_neighbor_dict(neighbor)
            )
        return grouped_data

    @staticmethod
    def _create_neighbor_dict(neighbor: Dict) -> Dict:
        """
        Create a dictionary for a neighbor.

        Args:
            neighbor (Dict): The neighbor data.

        Returns:
            Dict: The neighbor dictionary.
        """
        return {
            "interface_name": neighbor["if-name"],
            "level": neighbor["level"],
            "local_ipv4_address": neighbor["ipv4-address"],
            "isis_status": neighbor["state"],
            "holdtime": neighbor["holdtime"],
        }

    def _prepare_output_data(self, grouped_data: Dict) -> List[Dict]:
        """
        Prepare the output data.

        Args:
            grouped_data (Dict): The grouped data.

        Returns:
            List[Dict]: The output data.
        """
        output_data = [
            {
                "isis_neighbors_count": len(grouped_data),
                "isis-neighbors": self._prepare_neighbor_data(grouped_data),
                "field": self.filter_id,
                "device": self.device.hostname,
                "ip": self.device.host,
            }
        ]
        return output_data

    def _prepare_neighbor_data(self, grouped_data: Dict) -> List[Dict]:
        """
        Prepare the neighbor data.

        Args:
            grouped_data (Dict): The grouped data.

        Returns:
            List[Dict]: The neighbor data.
        """
        return [
            {
                "system-id": system_id,
                "local_interfaces_status": interfaces,
                "neighbor_status": 1
                if any(
                    interface["isis_status"] == "isis-adj-up"
                    for interface in interfaces
                )
                else 0,
            }
            for system_id, interfaces in grouped_data.items()
        ]
