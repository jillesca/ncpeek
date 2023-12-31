import os
from tempfile import TemporaryDirectory
import pytest
from ncpeek.utils.file_utils import (
    read_file,
    append_to_file,
    remove_path_from_filename,
    resolve_devices_path,
    is_valid_file_path,
    construct_default_devices_path,
    get_script_directory,
    resolve_filter_path,
    construct_default_filter_path,
)


def test_read_file():
    """
    Test reading content from a file.
    """
    with TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Test content")

        assert read_file(test_file) == "Test content"


def test_append_to_file():
    """
    Test appending text to a file.
    """
    with TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, "test.txt")

        append_to_file(test_file, "Test content")
        assert read_file(test_file) == "Test content"

        append_to_file(test_file, "\nMore content")
        assert read_file(test_file) == "Test content\nMore content"


def test_remove_path_from_filename():
    """
    Test removing path from a filename.
    """
    filename = "/path/to/test.txt"
    assert remove_path_from_filename(filename) == "test.txt"

    url = "http://example.com/test.txt"
    assert remove_path_from_filename(url) == url

    secure_url = "https://example.com/test.txt"
    assert remove_path_from_filename(secure_url) == secure_url


def test_is_valid_file_path():
    """
    Test if a filepath is an existing file.
    """
    with TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Test content")

        assert is_valid_file_path(test_file) == True

        assert is_valid_file_path("/non/existent/path") == False


def test_get_script_directory():
    """
    Test getting the directory of the script.
    """
    assert os.path.exists(get_script_directory())


def test_resolve_devices_path():
    """
    Test resolving the path of a devices file.
    """
    with TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Test content")

        assert resolve_devices_path(test_file) == test_file
        assert resolve_devices_path(
            "non_existent_file"
        ) == construct_default_devices_path("non_existent_file")


def test_construct_default_devices_path():
    """
    Test constructing the default path for a devices file.
    """
    filename = "test_file"
    expected_path = f"{get_script_directory()}/devices/{filename}"
    assert construct_default_devices_path(filename) == expected_path


def test_resolve_filter_path():
    """
    Test resolving the path of a filter file.
    """
    with TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Test content")

        assert resolve_filter_path(test_file) == test_file
        assert resolve_filter_path(
            "non_existent_file"
        ) == construct_default_filter_path("non_existent_file")


def test_construct_default_filter_path():
    """
    Test constructing the default path for a filter file.
    """
    filename = "test_file"
    expected_path = f"{get_script_directory()}/filters/{filename}"
    assert construct_default_filter_path(filename) == expected_path
