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
def config_fixture_path(tmp_path: Path) -> Path:
    temp_config_path = tmp_path / CONFIG_FILE
    return temp_config_path


class TestGet:
    @pytest.mark.parametrize(
        ("config_content", "key", "config_name", "env_var", "expected"),
        [
            # Existing value with CONFIG_ACTIVE set
            (
                "default:\n  key1: value1\n  key2: value2",
                "key1",
                None,
                "default",
                "value1",
            ),
            # Non-existing value
            (
                "default:\n  key1: value1\n  key2: value2",
                "non_existing_key",
                None,
                None,
                None,
            ),
            # Overwriting value with explicit config
            (
                "default:\n  key1: value1\n  key2: value2\n"
                "non-default:\n  key2: value3",
                "key2",
                "non-default",
                None,
                "value3",
            ),
            # Null default config
            (
                "default: ~\nnon-default:\n  key1: value1\n  key2: value2",
                "key1",
                None,
                "non-default",
                "value1",
            ),
        ],
        ids=[
            "existing_value",
            "non_existing_value",
            "overwriting_value",
            "null_default",
        ],
    )
    def test_get_scenarios(
        self,
        config_fixture_path,
        config_content,
        key,
        config_name,
        env_var,
        expected,
        monkeypatch,
    ):
        if env_var:
            monkeypatch.setenv("CONFIG_ACTIVE", env_var)
        config_fixture_path.write_text(config_content)
        result = get(key, file=config_fixture_path, config=config_name)
        assert result == expected

    def test_missing_default_key(self, config_fixture_path: Path):
        config_fixture_path.write_text("""
        environment:
            key1: value1
            key2: value2
        """)
        with pytest.raises(MissingDefaultConfigError):
            get(file=config_fixture_path)


class TestFindConfigFile:
    @pytest.mark.parametrize(
        ("file_exists", "should_raise"),
        [
            (True, False),  # existing file
            (False, True),  # non-existing file
        ],
        ids=["existing_file", "non_existing_file"],
    )
    def test_find_config(self, tmp_path, file_exists, should_raise):
        temp_config_path = tmp_path / CONFIG_FILE
        if file_exists:
            temp_config_path.write_text("dummy_content")

        if should_raise:
            with pytest.raises(FileNotFoundError):
                find_config_file("non_existing_file.yml", use_parent=False)
        else:
            config_path = find_config_file(temp_config_path, use_parent=False)
            assert config_path == temp_config_path


class TestReplaceEnvVars:
    @pytest.mark.parametrize(
        ("input_data", "expected_output"),
        [
            (
                {"key1": "$TEST_VAR", "key2": "value2"},
                {"key1": "replaced_value", "key2": "value2"},
            ),
            (["$TEST_VAR", "value2"], ["replaced_value", "value2"]),
        ],
        ids=["dict", "list"],
    )
    def test_replace_env_vars_basic(self, input_data, expected_output, monkeypatch):
        monkeypatch.setenv("TEST_VAR", "replaced_value")
        assert replace_env_vars(input_data) == expected_output

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
    def test_replace_env_vars_mixed_strings(
        self, input_value, env_vars, expected, monkeypatch
    ):
        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)

        result = replace_env_vars({"key": input_value})
        assert result["key"] == expected

    def test_replace_env_vars_nested_mixed(self, monkeypatch):
        monkeypatch.setenv("API_HOST", "api")
        monkeypatch.setenv("DOMAIN", "example.com")

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

    def test_replace_env_vars_backward_compatibility_missing_var(self):
        result = replace_env_vars({"key": "$MISSING_VAR"})
        assert result["key"] == "$MISSING_VAR"
