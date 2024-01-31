from typing import Optional, Union
from dataclasses import dataclass, field


@dataclass
class NetconfDevice:
    """
    This class represents a network device with its configurations.
    """

    host: str = None
    password: str = None
    username: str = None
    device_params: dict = field(default_factory=dict)
    hostname: Optional[str] = None
    port: Optional[int] = 830
    timeout: Optional[int] = 60
    hostkey_verify: Optional[Union[bool, str]] = False
    allow_agent: Optional[Union[bool, str]] = True
    look_for_keys: Optional[Union[bool, str]] = True

    def __post_init__(self):
        """
        Converts some attributes' string values to boolean.
        """
        self._check_required_fields()
        self.hostkey_verify = self.convert_str_to_bool(
            str_value=self.hostkey_verify
        )
        self.allow_agent = self.convert_str_to_bool(str_value=self.allow_agent)
        self.look_for_keys = self.convert_str_to_bool(
            str_value=self.look_for_keys
        )
        self._set_hostname()

    def _set_hostname(self) -> None:
        """
        Sets the hostname of the device if it is not already set.
        """
        if not self.hostname:
            self.hostname = self.host

    def _check_required_fields(self) -> None:
        """
        Validates that the required fields are provided.
        """
        missing_fields = []
        host = ""
        if not self.host:
            missing_fields.append("'Host'")
        else:
            host = self.host

        if not self.password:
            missing_fields.append("'Password'")
        if not self.username:
            missing_fields.append("'Username'")

        if missing_fields:
            fields = ", ".join(missing_fields)
            host_msg = f" for host '{host}'" if host else ""
            raise ValueError(
                f"Missing field(s){host_msg}: {fields}. These must be provided in JSON format."
            )

    @staticmethod
    def convert_str_to_bool(str_value: Union[bool, str]) -> bool:
        """
        This function parses boolean values from string representation.
        Needed as a string "False" in JSON is considered True in Python.
        """
        if isinstance(str_value, bool):
            return str_value
        if str_value.lower() == "true":
            return True
        if str_value.lower() == "false":
            return False
        else:
            raise ValueError(
                f"Invalid boolean value: {str_value} for NetconfDevice option."
            )
