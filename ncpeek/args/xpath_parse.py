import re


def extract_xpath(netconf_filter: str) -> tuple:
    """
    Extract xpath from a netconf filter string.

    Args: netconf_filter (str): The netconf filter string.

    Returns: tuple: A tuple containing the type of filter and the extracted xpath.
    """
    if ":" not in netconf_filter:
        return ("xpath", netconf_filter)

    if "http://" in netconf_filter or "https://" in netconf_filter:
        return _extract_xpath_from_url(netconf_filter=netconf_filter)

    return _extract_xpath_without_url(netconf_filter=netconf_filter)


def _extract_xpath_from_url(netconf_filter: str) -> tuple:
    """
    Extract xpath from a netconf filter string that contains a URL.

    Args: netconf_filter (str): The netconf filter string.

    Returns: tuple: A tuple containing the type of filter and the extracted xpath.
    """
    ns_xpath = re.search(r"(https*:\/\/\S+):(\S+)", netconf_filter)
    ns = ns_xpath.group(1)
    select = ns_xpath.group(2)
    return ("xpath", ({"ns0": ns}, select))


def _extract_xpath_without_url(netconf_filter: str) -> tuple:
    """
    Extract xpath from a netconf filter string that does not contain a URL.

    Args: netconf_filter (str): The netconf filter string.

    Returns: tuple: A tuple containing the type of filter and the extracted xpath.
    """
    ns, select = netconf_filter.split(":")
    return ("xpath", ({"ns0": ns}, select))
