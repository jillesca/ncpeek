import argparse
import pytest
from ncpeek.args.arg_parser import create_argument_parser


def test_create_argument_parser():
    """
    Test creation of argument parser with mutually exclusive arguments.
    """
    # Create the parser
    parser = create_argument_parser()

    # Check the type of the parser
    assert isinstance(parser, argparse.ArgumentParser)

    # Check that the required arguments are present
    assert any(action.dest == "device_settings" for action in parser._actions)
    assert any(action.dest == "xml_filter" for action in parser._actions)
    assert any(action.dest == "xpath_filter" for action in parser._actions)
