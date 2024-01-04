import os
from pathlib import Path

DEFAULT_DEVICES_DIR = "devices"
DEFAULT_FILTER_DIR = "filters"


def read_settings(filename: str) -> str:
    """Read device settings"""
    file = resolve_path(filename=filename, kind="settings")
    return read_file(filename=file)


def read_filter(filename: str) -> str:
    """Read filter xml file"""
    file = resolve_path(filename=filename, kind="filter")
    return read_file(filename=file)


def resolve_path(filename: str, kind: str) -> str:
    """Resolve the path for files."""
    path = resolve_absolute_path(filename=filename)
    if is_valid_file_path(filepath=path):
        return path
    if "settings" in kind:
        return construct_default_devices_path(filename=filename)
    return construct_default_filter_path(filename=filename)


def resolve_absolute_path(filename: str) -> str:
    """Considers symlinks and home directory relative paths"""
    return os.path.realpath(os.path.expanduser(filename))


def is_valid_file_path(filepath: str) -> bool:
    """Check if a filepath is an existing file."""
    return os.path.exists(filepath) and os.path.isfile(filepath)


def construct_default_devices_path(filename: str) -> str:
    """Construct the default path for a devices file."""
    return f"{get_script_directory()}/{DEFAULT_DEVICES_DIR}/{filename}"


def construct_default_filter_path(filename: str) -> str:
    """Construct the default path for a filter file."""
    return f"{get_script_directory()}/{DEFAULT_FILTER_DIR}/{filename}"


def get_script_directory() -> str:
    """Get the directory of the script."""
    return Path(os.path.abspath(os.path.dirname(__file__))).parents[0]


def read_file(filename: str) -> str:
    """Read content from a file."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as err:
        raise ValueError(f"Unable to open file. Error: {err=}") from err


def append_to_file(filename: str, text: str) -> None:
    """Append text to a file."""
    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(text)
    except Exception as err:
        raise ValueError(f"Unable to write to file. Error: {err=}") from err


def remove_path_from_filename(filename: str) -> str:
    """Remove the path from a filename, keeping the base name.
    If filename starts with http:// or https://, return as is."""
    if "http://" in filename or "https://" in filename:
        return filename
    return os.path.basename(filename)
