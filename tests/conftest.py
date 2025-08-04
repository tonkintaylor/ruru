from pathlib import Path

import pytest

ROOT_PATH = Path(__file__).parent.parent

collect_ignore_glob = ["assets/**"]
# Ignore doctests from cli.py module
collect_ignore = [str(ROOT_PATH / "src" / "ruru" / "cli.py")]
pytest_plugins = []


@pytest.fixture(scope="session")
def assets_dir() -> Path:
    """Return a path to the test assets directory."""
    return ROOT_PATH / "tests" / "assets"
