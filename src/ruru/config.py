"""Functionality for reading YAML configuration file.

Inspired by the R package `config` (https://rstudio.github.io/config/).
"""

import os
import re
from pathlib import Path
from typing import Any, overload

import yaml


class MissingDefaultConfigError(Exception):
    """Raised when the configuration file does not contain a 'default' key."""


def get(
    value: str | None = None,
    config: str | None = None,
    file: str | Path = "config.yml",
    *,
    use_parent: bool = True,
) -> Any:
    """Load and merge configuration settings from a YAML file.

    This function reads a YAML file containing a 'default' field and merges it
    with the settings of the specified environment. It can also read a specific
    value from the merged configuration settings. Environment variables in the form
    $VAR_NAME are replaced with their values. This supports both pure environment
    variables ($VAR) and mixed strings with multiple variables
    (e.g., https://$HOST.$DOMAIN). Missing environment variables are replaced with
    empty strings. It can handle nested dictionaries and lists.

    Inspired by the R package `config` (https://rstudio.github.io/config/).

    We highly recommend you:

    - Use at most two hierarchy levels for your config files. This will make it
      easier to find the config values you need.
    - Separate yaml files for different components. This will make your config
      files more organized and manageable.

    Args:
        value: Name of the value to read (None to read all values).
        config: The environment or configuration name to load. If None,
            the environment is determined by the CONFIG_ACTIVE environment variable
            or defaults to "default".
        file: Configuration file to read from (defaults to "config.yml"). If the file
            isn't found at the location specified, then parent directories are
            searched for a file of the same name.
        use_parent: True to scan parent directories for configuration files if the
            specified config file isn't found.

    Returns:
        The requested value or a dictionary containing the merged configuration
        settings.
    """
    config_file = find_config_file(file, use_parent=use_parent)

    if config is None:
        config = os.getenv("CONFIG_ACTIVE", default="default")

    with config_file.open(mode="r", encoding="utf-8") as config_file_handle:
        config_data: Any = yaml.safe_load(config_file_handle)

    if not isinstance(config_data, dict):
        msg = f"Configuration file '{config_file}' must contain a dictionary."
        raise TypeError(msg)

    if "default" not in config_data:
        msg = f"Configuration file '{config_file}' does not contain a 'default' key."
        raise MissingDefaultConfigError(msg)

    default_config = config_data["default"]
    environment_config = config_data.get(config, {})

    if not isinstance(environment_config, dict):
        msg = f"Configuration for '{config}' in '{config_file}' must be a dictionary."
        raise TypeError(msg)

    if isinstance(default_config, dict) and default_config:
        merged_config = {**default_config, **environment_config}
    elif isinstance(environment_config, dict) and environment_config:
        merged_config = environment_config
    else:
        msg = (
            f"Configuration for either 'default' or '{config}' in '{config_file}' "
            "must be non-empty dictionaries."
        )
        raise TypeError(msg)

    merged_config = replace_env_vars(merged_config)

    if value is None:
        return merged_config
    return merged_config.get(value)


def find_config_file(file: str | Path, *, use_parent: bool) -> Path:
    """Find the specified configuration file in the current or parent directories.

    This function searches for the specified configuration file in the current
    directory and, if not found, optionally continues searching in parent
    directories.

    Args:
        file: Name of the configuration file to search for.
        use_parent: True to scan parent directories for the configuration
            file if it's not found in the current directory.

    Returns:
        The absolute path of the found configuration file.
    """
    current_path = Path().cwd()

    while current_path is not None:
        config_file = current_path / file
        if config_file.exists() and config_file.is_file():
            return config_file

        if not use_parent:
            break

        current_path = current_path.parent if current_path.parent != current_path else None

    msg = f"Configuration file '{file}' not found."
    raise FileNotFoundError(msg)


@overload
def replace_env_vars(data: dict) -> dict: ...
@overload
def replace_env_vars(data: list) -> list: ...
def replace_env_vars(data: dict | list) -> dict | list:
    """Replace environment variables in strings with their values.

    This function handles both pure environment variables ($VAR) and mixed
    strings containing one or more environment variables (e.g., https://$VAR1.$VAR2).
    Environment variables not found are replaced with empty strings.

    Args:
        data: Dictionary or list containing configuration data.

    Returns:
        Dictionary or list with environment variables replaced by their values.

    Examples:
        >>> os.environ["DB_HOST"] = "localhost"
        >>> replace_env_vars({"url": "$DB_HOST"})
        {'url': 'localhost'}
        >>> replace_env_vars({"url": "https://$DB_HOST:5432"})
        {'url': 'https://localhost:5432'}
    """
    if isinstance(data, dict):
        return {key: _replace_item(val) for key, val in data.items()}
    if isinstance(data, list):
        return [_replace_item(val) for val in data]

    return data


@overload
def _replace_item(item: str) -> str: ...
@overload
def _replace_item(item: dict) -> dict: ...
@overload
def _replace_item(item: list) -> list: ...
def _replace_item(item: str | dict | list) -> str | dict | list:
    """Helper function to replace an individual item."""
    if isinstance(item, str) and "$" in item:
        return _expand_env_vars(item)
    if isinstance(item, dict | list):
        return replace_env_vars(item)
    return item


def _replace_var(match: re.Match[str]) -> str:
    """Replace a single environment variable match with its value.

    Args:
        match: Regular expression match object for an environment variable.

    Returns:
        The environment variable value, or empty string if not set.
    """
    var_name = match.group(1)
    return os.getenv(var_name, "")


def _expand_env_vars(value: str) -> str:
    """Expand environment variables in a string with mixed content.

    Finds all $VAR_NAME patterns in the string and replaces them with their
    corresponding environment variable values. If an environment variable is
    not set, it is replaced with an empty string. For backward compatibility,
    if the entire string is a single pure environment variable (e.g., "$VAR")
    and it's not found, the original string is returned.

    Args:
        value: String that may contain one or more $VAR_NAME patterns.

    Returns:
        String with all $VAR_NAME patterns replaced by their environment
        variable values or empty strings if not set.

    Examples:
        >>> os.environ["APP_NAME"] = "myapp"
        >>> os.environ["DOMAIN"] = "example.com"
        >>> _expand_env_vars("https://$APP_NAME.$DOMAIN")
        'https://myapp.example.com'
        >>> _expand_env_vars("$VAR1-$VAR2")
        'value1-value2'
    """
    pattern = r"\$([A-Z_][A-Z0-9_]*)"

    # Check if it's a pure env var for backward compatibility
    match = re.fullmatch(pattern, value)
    if match:
        var_name = match.group(1)
        return os.getenv(var_name, default=value)

    # Handle mixed strings
    return re.sub(pattern, _replace_var, value)
