import os
from collections.abc import Generator
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
def config_fixture_path(tmp_path: Path) -> Generator[Path]:
    temp_config_path = tmp_path / CONFIG_FILE
    yield temp_config_path
    if "CONFIG_ACTIVE" in os.environ:
        del os.environ["CONFIG_ACTIVE"]


class TestGet:
    def test_existing_value(self, config_fixture_path: Path):
        os.environ["CONFIG_ACTIVE"] = "default"
        config_fixture_path.write_text("""
        default:
            key1: value1
            key2: value2
        """)
        assert get("key1", file=config_fixture_path) == "value1"

    def test_non_existing_value(self, config_fixture_path: Path):
        config_fixture_path.write_text("""
        default:
            key1: value1
            key2: value2
        """)
        assert get("non_existing_key", file=config_fixture_path) is None

    def test_overwriting_value(self, config_fixture_path: Path):
        config_fixture_path.write_text("""
        default:
            key1: value1
            key2: value2
        non-default:
            key2: value3
        """)
        assert get("key2", file=config_fixture_path, config="non-default") == "value3"

    def test_null_default(self, config_fixture_path: Path):
        os.environ["CONFIG_ACTIVE"] = "non-default"
        config_fixture_path.write_text("""
        default: ~
        non-default:
            key1: value1
            key2: value2
        """)
        assert get("key1", file=config_fixture_path) == "value1"

    def test_missing_default_key(self, config_fixture_path: Path):
        config_fixture_path.write_text("""
        environment:
            key1: value1
            key2: value2
        """)
        with pytest.raises(MissingDefaultConfigError):
            get(file=config_fixture_path)


class TestFindConfigFile:
    def test_existing_file(self, tmp_path: Path):
        temp_config_path = tmp_path / CONFIG_FILE
        temp_config_path.write_text("dummy_content")
        config_path = find_config_file(temp_config_path, use_parent=False)
        assert config_path == temp_config_path

    def test_non_existing_file(self):
        with pytest.raises(FileNotFoundError):
            find_config_file("non_existing_file.yml", use_parent=False)


class TestReplaceEnvVars:
    def test_replace_env_vars_dict(self):
        os.environ["TEST_VAR"] = "replaced_value"
        input_data = {"key1": "$TEST_VAR", "key2": "value2"}
        expected_output = {"key1": "replaced_value", "key2": "value2"}
        assert replace_env_vars(input_data) == expected_output
        del os.environ["TEST_VAR"]

    def test_replace_env_vars_list(self):
        os.environ["TEST_VAR"] = "replaced_value"
        input_data = ["$TEST_VAR", "value2"]
        expected_output = ["replaced_value", "value2"]
        assert replace_env_vars(input_data) == expected_output
        del os.environ["TEST_VAR"]

    @pytest.mark.parametrize(
        ("input_value", "env_vars", "expected"),
        [
            ("https://$APP_NAME", {"APP_NAME": "myapp"}, "https://myapp"),
            (
                "$APP_NAME.azurecontainer.io",
                {"APP_NAME": "myapp"},
                "myapp.azurecontainer.io",
            ),
            ("$VAR1$VAR2", {"VAR1": "hello", "VAR2": "world"}, "helloworld"),
            ("$VAR1-$VAR2", {"VAR1": "app", "VAR2": "env"}, "app-env"),
            (
                "https://$APP_NAME.$DOMAIN",
                {"APP_NAME": "myapp", "DOMAIN": "eastus.azurecontainer.io"},
                "https://myapp.eastus.azurecontainer.io",
            ),
            ("$SINGLE_VAR", {"SINGLE_VAR": "value"}, "value"),
            ("https://$MISSING_VAR.com", {}, "https://.com"),
            ("https://static.com", {}, "https://static.com"),
        ],
    )
    def test_replace_env_vars_mixed_strings(self, input_value, env_vars, expected):
        for key, value in env_vars.items():
            os.environ[key] = value

        try:
            result = replace_env_vars({"key": input_value})
            assert result["key"] == expected
        finally:
            for key in env_vars:
                if key in os.environ:
                    del os.environ[key]

    def test_replace_env_vars_nested_mixed(self):
        os.environ["API_HOST"] = "api"
        os.environ["DOMAIN"] = "example.com"

        input_data = {
            "api_url": "https://$API_HOST.$DOMAIN/v1",
            "nested": {"endpoint": "$API_HOST/endpoint"},
            "list": ["$API_HOST", "https://$DOMAIN"],
        }

        expected = {
            "api_url": "https://api.example.com/v1",
            "nested": {"endpoint": "api/endpoint"},
            "list": ["api", "https://example.com"],
        }

        result = replace_env_vars(input_data)
        assert result == expected

        del os.environ["API_HOST"]
        del os.environ["DOMAIN"]

    def test_replace_env_vars_backward_compatibility_missing_var(self):
        result = replace_env_vars({"key": "$MISSING_VAR"})
        assert result["key"] == "$MISSING_VAR"
