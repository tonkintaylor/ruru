"""Tests for the symbols module."""

import sys
from io import StringIO

import pytest

from ruru import cli


# Custom StringIO class with None encoding for testing
class StdoutWithNoneEncoding(StringIO):
    encoding = None  # type: ignore[assignment]


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


@pytest.mark.parametrize(
    ("func", "expected_ascii"),
    [
        (cli.bullet, "*"),
        (cli.tick, "v"),
        (cli.cross, "x"),
        (cli.warning, "!"),
        (cli.info, "i"),
        (cli.line, "-"),
    ],
)
def test_symbols_with_none_stdout_encoding(monkeypatch, func, expected_ascii):
    """Test symbol functions handle None stdout.encoding gracefully."""
    mock_stdout = StdoutWithNoneEncoding()
    monkeypatch.setattr(sys, "stdout", mock_stdout)

    # Should not crash, should fall back to ASCII
    result = func()
    assert result == expected_ascii


@pytest.mark.parametrize(
    ("func", "expected_ascii"),
    [
        (cli.bullet, "*"),
        (cli.tick, "v"),
        (cli.cross, "x"),
        (cli.warning, "!"),
        (cli.info, "i"),
    ],
)
def test_symbols_with_missing_stdout(monkeypatch, func, expected_ascii):
    """Test symbol functions handle missing stdout gracefully."""
    monkeypatch.setattr(sys, "stdout", None)

    # Should not crash, should fall back to ASCII
    result = func()
    assert result == expected_ascii
