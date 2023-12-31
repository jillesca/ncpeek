from typing import Optional
from dataclasses import dataclass
from ncclient import manager
from ncpeek.netconf_devices import NetconfDevice


@dataclass
class NetconfSessionManager:
    """Handles the network configuration session for a device."""

    device: NetconfDevice
    netconf_filter: Optional[str] = None

    def retrieve_data(self, netconf_filter: str) -> str:
        """
        Retrieves data from the device using the specified Netconf filter.

        Args: netconf_filter: The filter to use for the Netconf GET operation.
        Returns: The result of the Netconf GET operation.
        """
        self.netconf_filter = netconf_filter
        return self._perform_operation(operation="GET")

    def _perform_operation(self, operation: str) -> str:
        """
        Executes the specified operation on the device.

        Args: operation: The operation to perform.
        Returns: The result of the operation.
        """
        with self._establish_connection() as session:
            match operation:
                case "GET":
                    return session.get(self.netconf_filter)

    def _establish_connection(self) -> manager:
        """
        Establishes a Netconf session with the device.

        Returns: The established session.
        """
        return manager.connect(
            host=self.device.host,
            port=self.device.port,
            username=self.device.username,
            password=self.device.password,
            hostkey_verify=self.device.hostkey_verify,
            device_params=self.device.device_params,
            timeout=self.device.timeout,
            allow_agent=self.device.allow_agent,  # use for old ssh servers, like XR 7.3.2
            look_for_keys=self.device.look_for_keys,  # use for old ssh servers, like XR 7.3.2
        )
