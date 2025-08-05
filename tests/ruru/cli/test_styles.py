"""Tests for the styles module."""

import pytest

from ruru import cli


@pytest.mark.parametrize("style_func", [cli.bold, cli.dim, cli.italic, cli.underline])
def test_text_style_functions_return_styled_text(style_func):
    """Test text style functions return styled text."""
    result = style_func("test")
    assert result != "test"


@pytest.mark.parametrize(
    "color_func",
    [cli.red, cli.green, cli.yellow, cli.blue, cli.magenta, cli.cyan, cli.orange],
)
def test_convenience_color_functions_return_colored_text(color_func):
    """Test convenience color functions return colored text."""
    result = color_func("test")
    assert result != "test"


@pytest.mark.parametrize(
    "color_name",
    [
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
        "bright_black",
        "bright_red",
        "bright_green",
        "bright_yellow",
        "bright_blue",
        "bright_magenta",
        "bright_cyan",
        "bright_white",
    ],
)
def test_color_function_returns_colored_text(color_name):
    """Test color function returns colored text for valid color names."""
    result = cli.color("test", color_name)
    assert result != "test"
