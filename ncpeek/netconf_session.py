from typing import Optional
from dataclasses import dataclass
from ncclient import manager
from ncpeek.netconf_devices import NetconfDevice


@dataclass
class NetconfSession:
    """Handles the netconf session for a device."""

    device: NetconfDevice
    netconf_filter: str
    operation: str
    result: Optional[str] = None

    def __post_init__(self) -> None:
        """
        Executes the netconf operation.

        Returns: The result of the Netconf  operation.
        """
        self.result = self._perform_operation()

    def reply(self) -> str:
        """retrieves rpc reply from operation performed.

        Returns:
            str: rpc result from data_xml attribute.
        """
        return self.result.data_xml

    def _perform_operation(self) -> str:
        """
        Executes the specified operation on the device.

        Args: operation: The operation to perform.
        Returns: The result of the operation.
        """
        with self._establish_connection() as session:
            match self.operation:
                case "fetch":
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
