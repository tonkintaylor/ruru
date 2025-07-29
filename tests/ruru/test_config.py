import os
from pathlib import Path

import pytest

from ruru.config import (
    MissingDefaultConfigError,
    find_config_file,
    get,
    replace_env_vars,
)

CONFIG_FILE = "config.yml"


@pytest.fixture
def config_fixture(tmp_path: Path):
    temp_config_path = tmp_path / CONFIG_FILE
    yield temp_config_path
    if "CONFIG_ACTIVE" in os.environ:
        del os.environ["CONFIG_ACTIVE"]


class TestGet:
    def test_existing_value(self, config_fixture):
        os.environ["CONFIG_ACTIVE"] = "default"
        config_fixture.write_text("""
        default:
            key1: value1
            key2: value2
        """)
        assert get("key1", file=config_fixture) == "value1"

    def test_non_existing_value(self, config_fixture):
        config_fixture.write_text("""
        default:
            key1: value1
            key2: value2
        """)
        os.environ["CONFIG_ACTIVE"] = config_fixture.as_posix()
        assert get("non_existing_key", file=config_fixture) is None

    def test_overwriting_value(self, config_fixture):
        config_fixture.write_text("""
        default:
            key1: value1
            key2: value2
        non-default:
            key2: value3
        """)
        os.environ["CONFIG_ACTIVE"] = config_fixture.as_posix()
        assert get("key2", file=config_fixture, config="non-default") == "value3"

    def test_null_default(self, config_fixture):
        os.environ["CONFIG_ACTIVE"] = "non-default"
        config_fixture.write_text("""
        default: ~
        non-default:
            key1: value1
            key2: value2
        """)
        assert get("key1", file=config_fixture) == "value1"

    def test_missing_default_key(self, config_fixture):
        config_fixture.write_text("""
        environment:
            key1: value1
            key2: value2
        """)
        with pytest.raises(MissingDefaultConfigError):
            get(file=config_fixture)


class TestFindConfigFile:
    def test_existing_file(self, tmp_path: Path):
        """An existing file."""
        temp_config_path = tmp_path / CONFIG_FILE
        temp_config_path.write_text("dummy_content")
        config_path = find_config_file(temp_config_path, use_parent=False)
        assert config_path == temp_config_path

    def test_non_existing_file(self):
        with pytest.raises(FileNotFoundError):
            find_config_file("non_existing_file.yml", use_parent=False)


class TestReplaceEnvVars:
    def test_replace_env_vars_dict(self):
        """Test that replace_env_vars replaces environment variables in a dictionary."""
        os.environ["TEST_VAR"] = "replaced_value"
        input_data = {"key1": "$TEST_VAR", "key2": "value2"}
        expected_output = {"key1": "replaced_value", "key2": "value2"}
        assert replace_env_vars(input_data) == expected_output
        del os.environ["TEST_VAR"]

    def test_replace_env_vars_list(self):
        """Test that replace_env_vars replaces environment variables in a list."""
        os.environ["TEST_VAR"] = "replaced_value"
        input_data = ["$TEST_VAR", "value2"]
        expected_output = ["replaced_value", "value2"]
        assert replace_env_vars(input_data) == expected_output
        del os.environ["TEST_VAR"]
