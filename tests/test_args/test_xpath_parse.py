import pytest

from ncpeek.args.xpath_parse import (
    extract_xpath,
)


def test_extract_xpath():
    """
    Test extracting xpath from a netconf filter string.
    """
    # Test with a http in the netconf filter
    assert extract_xpath(
        "http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper:interfaces/interface"
    ) == (
        "xpath",
        (
            {"ns0": "http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper"},
            "interfaces/interface",
        ),
    )

    # Test with a https in the netconf filter
    assert extract_xpath(
        "https://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper:interfaces/interface"
    ) == (
        "xpath",
        (
            {"ns0": "https://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper"},
            "interfaces/interface",
        ),
    )

    # Test with a namespace in the netconf filter
    assert extract_xpath("namespace:filter") == (
        "xpath",
        ({"ns0": "namespace"}, "filter"),
    )

    # Test with no namespace or URL in the netconf filter
    assert extract_xpath("interfaces/interface") == (
        "xpath",
        "interfaces/interface",
    )
