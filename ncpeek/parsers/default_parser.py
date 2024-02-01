from ncpeek.netconf_parsers import Parser
from ncpeek.netconf_devices import NetconfDevice
from ncpeek.parsers.remove_namespaces import (
    remove_namespaces_from_dict,
)


class DefaultParser(Parser):
    """
    A default parser which translate the rcp reply to a generic structure.
    """

    def parse(
        self,
        data_to_parse: dict,
        device: NetconfDevice,
        netconf_filter_id: str,
    ) -> list[dict]:
        """
        Parse data to a generic structure without any logic.

        Args:
            data_to_parse (Dict): The data to parse.
            device (NetconfDevice): The device the data is related to.
            netconf_filter_id (str): The filter ID used for netconf.

        Returns:
            List[Dict]: The parsed data.
        """
        data = remove_namespaces_from_dict(data=data_to_parse["data"])
        return [
            {
                "ip": device.host,
                "device": device.hostname,
                "field": netconf_filter_id,
                "data": data,
            }
        ]
