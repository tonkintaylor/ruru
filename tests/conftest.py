from pathlib import Path
from unittest.mock import Mock

import pytest

collect_ignore_glob = ["assets/**"]
pytest_plugins = []


@pytest.fixture(scope="session")
def assets_dir() -> Path:
    """Return a path to the test assets directory."""
    return Path(__file__).parent / "assets"


@pytest.fixture(autouse=True)
def set_terminal_width(monkeypatch):
    """Mock terminal size for consistent CLI testing."""
    mock_size = Mock()
    mock_size.columns = 100
    mock_size.lines = 50
    monkeypatch.setattr("os.get_terminal_size", lambda fd=None: mock_size)  # noqa: ARG005
