from ncpeek.netconf_parsers import Parser
from ncpeek.factory.factory_parsers import get_parser
from ncpeek.factory.factory_mappings import PARSER_MAPPING


def test_parser_mapping_structure():
    """
    Test the structure of the PARSER_MAPPING dictionary.
    """
    for key, value in PARSER_MAPPING.items():
        assert isinstance(key, str)
        assert isinstance(value, dict)
        assert "module" in value
        assert "class" in value
        assert isinstance(value["module"], str)
        assert isinstance(value["class"], str)


def test_get_parser():
    """
    Test getting a parser instance based on the provided Netconf filter.
    """
    # We'll test for each key in the PARSER_MAPPING
    for parser_key in PARSER_MAPPING.keys():
        parser_instance = get_parser(parser_key)

        # Check that the returned object is an instance of Parser
        assert isinstance(parser_instance, Parser)

        # Check that the instance has a parse method
        assert hasattr(parser_instance, "parse")
