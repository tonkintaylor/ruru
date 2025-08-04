"""Functionality for reading YAML configuration file.

Inspired by the R package `config` (https://rstudio.github.io/config/).
"""

import os
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
    value from the merged configuration settings. If the YAML file contains a
    value that starts with '$', the function evaluates it as an environment
    variable using os.getenv() and assigns the returned value to the key. It can
    handle nested dictionaries and lists.

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

        current_path = (
            current_path.parent if current_path.parent != current_path else None
        )

    msg = f"Configuration file '{file}' not found."
    raise FileNotFoundError(msg)


@overload
def replace_env_vars(data: dict) -> dict: ...
@overload
def replace_env_vars(data: list) -> list: ...
def replace_env_vars(data: dict | list) -> dict | list:
    """Replace values starting with '$' with corresponding environment variables.

    Args:
        data: Dictionary or list containing configuration data.

    Returns:
        Dictionary or list with values starting with '$' replaced by environment
        variables.
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
    if isinstance(item, str) and item.startswith("$"):
        env_var = item[1:]
        return os.getenv(env_var, default=item)
    if isinstance(item, dict | list):
        return replace_env_vars(item)
    return item
