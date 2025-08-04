"""Tests for the symbols module."""

import pytest

from ruru.cli.symbols import (
    bullet,
    corner,
    cross,
    info,
    line,
    tick,
    tree_end,
    tree_mid,
    warning,
)


@pytest.mark.parametrize(
    ("func", "expected_symbols"),
    [
        (tick, ("✔", "v")),
        (cross, ("✖", "x")),
        (warning, ("⚠", "!")),
        (info, ("ℹ", "i")),
        (bullet, ("•", "*")),
        (line, ("─", "-")),
        (corner, ("└", "+")),
        (tree_mid, ("├", "+")),
        (tree_end, ("└", "+")),
    ],
)
def test_convenience_functions_return_expected_symbols(func, expected_symbols):
    """Test convenience functions return expected Unicode or ASCII symbols."""
    result = func()
    assert result in expected_symbols
