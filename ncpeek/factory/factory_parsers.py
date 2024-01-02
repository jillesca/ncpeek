from ncpeek.netconf_parsers import Parser
from ncpeek.factory.factory_mappings import PARSER_MAPPING


def get_parser(netconf_filter: str) -> Parser:
    """
    Returns a parser instance based on the provided Netconf filter.

    Args: netconf_filter: The Netconf filter ID.
    Returns: An instance of the appropriate parser.
    """

    parser_config = PARSER_MAPPING.get(
        netconf_filter, PARSER_MAPPING["default_parser"]
    )

    parser_module = __import__(
        parser_config["module"], fromlist=[parser_config["class"]]
    )
    # The last () in the line parser_instance is used to instantiate the class.
    parser_instance = getattr(parser_module, parser_config["class"])()

    return parser_instance
