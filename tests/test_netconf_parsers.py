import pytest
from ncpeek.netconf_parsers import Parser
from ncpeek.netconf_devices import NetconfDevice


class TestParser(Parser):
    """
    A subclass of Parser for testing purposes.
    """

    @classmethod
    def parse(
        cls,
        data_to_parse: dict,
        net_device: NetconfDevice,
        netconf_filter_id: str,
    ):
        return ["parsed data"]


def test_parser_classmethod_exists():
    """
    Test that the parse classmethod exists in the Parser subclass.
    """
    assert hasattr(TestParser, "parse")


def test_parser_raises_not_implemented():
    """
    Test that calling parse on the Parser base class raises a NotImplementedError.
    """
    with pytest.raises(NotImplementedError):
        Parser.parse(
            {},
            NetconfDevice(host="localhost", username="user", password="pass"),
            "filter_id",
        )


def test_parser_subclass_implementation():
    """
    Test the parse method of the Parser subclass.
    """
    net_device = NetconfDevice(
        host="localhost", username="user", password="pass"
    )
    data_to_parse = {"key": "value"}
    netconf_filter_id = "filter_id"

    parsed_data = TestParser.parse(
        data_to_parse, net_device, netconf_filter_id
    )

    assert parsed_data == ["parsed data"]
