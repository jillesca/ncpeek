from typing import List
from abc import ABC, abstractmethod
from ncpeek.netconf_devices import NetconfDevice


class Parser(ABC):
    """
    This is an abstract base class for parsers. It enforces the implementation
    of the 'parse' method in any derived class.
    """

    @classmethod
    @abstractmethod
    def parse(
        cls,
        data_to_parse: dict,
        net_device: NetconfDevice,
        netconf_filter_id: str,
    ) -> List:
        """
        This is an abstract method that must be implemented in any derived class.
        It should parse the given data and return a list.

        Args:
            data_to_parse: The data to parse.
            net_device: The network device.
            netconf_filter_id: The filter ID for netconf.

        Returns: A list of parsed data.
        """
        raise NotImplementedError(
            "Subclasses must implement this parse method."
        )
