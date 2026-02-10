"""Tests for the symbols module."""

import sys
from unittest.mock import Mock

import pytest

from ruru import cli


@pytest.mark.parametrize(
    ("func", "expected_symbols"),
    [
        (cli.tick, ("✔", "v")),
        (cli.cross, ("✖", "x")),
        (cli.warning, ("⚠", "!")),
        (cli.info, ("ℹ", "i")),
        (cli.bullet, ("•", "*")),
        (cli.line, ("─", "-")),
        (cli.corner, ("└", "+")),
        (cli.tree_mid, ("├", "+")),
        (cli.tree_end, ("└", "+")),
    ],
)
def test_convenience_functions_return_expected_symbols(func, expected_symbols):
    """Test convenience functions return expected Unicode or ASCII symbols."""
    result = func()
    assert result in expected_symbols


def test_symbols_with_none_stdout_encoding(monkeypatch):
    """Test symbol functions handle None stdout.encoding gracefully."""
    mock_stdout = Mock()
    mock_stdout.encoding = None
    monkeypatch.setattr(sys, "stdout", mock_stdout)

    # Should not crash, should fall back to ASCII
    result = cli.bullet()
    assert result == "*"


def test_symbols_with_missing_stdout(monkeypatch):
    """Test symbol functions handle missing stdout gracefully."""
    monkeypatch.setattr(sys, "stdout", None)

    # Should not crash, should fall back to ASCII
    result = cli.tick()
    assert result == "v"
