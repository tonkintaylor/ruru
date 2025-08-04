"""Tests for the symbols module."""

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
