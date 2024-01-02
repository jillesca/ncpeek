import json
import xml.etree.ElementTree as ET
import xmltodict


def is_string_valid_xml(xml_string):
    """validates a string is valid xml

    Args:
        xml_string (str): string validating xml

    Returns:
        bool: true if the string is valid xml otherwise false
    """
    try:
        ET.fromstring(xml_string)
        return True
    except ET.ParseError:
        return False


def convert_json_to_dict(json_string: str) -> dict:
    """
    Convert JSON string to dictionary.

    Args: json_string (str): The JSON string.

    Returns: dict: The converted dictionary.
    """
    return json.loads(json_string)


def convert_xml_to_dict(xml_string: str) -> dict:
    """
    Convert XML string to dictionary.

    Args:  xml_string (str): The XML string.

    Returns: dict: The converted dictionary.
    """
    return xmltodict.parse(xml_string)


def convert_dict_to_json(input_dict: dict) -> str:
    """
    Convert dictionary to JSON string.

    Args: input_dict (dict): The dictionary.

    Returns: str: The converted JSON string.
    """
    return json.dumps(input_dict)
