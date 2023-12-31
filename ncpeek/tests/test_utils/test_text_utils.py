import pytest

from ncpeek.utils.text_utils import (
    convert_json_to_dict,
    convert_xml_to_dict,
    convert_dict_to_json,
)


def test_convert_json_to_dict():
    """
    Test converting a JSON string to a dictionary.
    """
    json_string = '{"key": "value"}'
    assert convert_json_to_dict(json_string) == {"key": "value"}


def test_convert_xml_to_dict():
    """
    Test converting an XML string to a dictionary.
    """
    xml_string = "<root><key>value</key></root>"
    assert convert_xml_to_dict(xml_string) == {"root": {"key": "value"}}


def test_convert_dict_to_json():
    """
    Test converting a dictionary to a JSON string.
    """
    input_dict = {"key": "value"}
    assert convert_dict_to_json(input_dict) == '{"key": "value"}'
