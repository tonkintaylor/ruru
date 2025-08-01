"""Tests for CLI styles module."""

import os

from ruru.cli.styles import (
    _supports_color,
    blue,
    bold,
    color,
    cyan,
    dim,
    green,
    italic,
    magenta,
    red,
    underline,
    yellow,
)


class TestSupportsColor:
    def test_no_color_env_var(self, monkeypatch):
        """Test that NO_COLOR environment variable disables color."""
        monkeypatch.setenv("NO_COLOR", "1")
        assert not _supports_color()

    def test_force_color_env_var(self, monkeypatch):
        """Test that FORCE_COLOR environment variable enables color."""
        monkeypatch.setenv("FORCE_COLOR", "1")
        monkeypatch.delenv("NO_COLOR", raising=False)
        assert _supports_color()


class TestTextStyles:
    def test_bold(self):
        """Test bold text styling."""
        result = bold("test")
        assert isinstance(result, str)
        assert "test" in result

    def test_dim(self):
        """Test dim text styling."""
        result = dim("test")
        assert isinstance(result, str)
        assert "test" in result

    def test_italic(self):
        """Test italic text styling."""
        result = italic("test")
        assert isinstance(result, str)
        assert "test" in result

    def test_underline(self):
        """Test underline text styling."""
        result = underline("test")
        assert isinstance(result, str)
        assert "test" in result


class TestColors:
    def test_basic_colors(self):
        """Test basic color functions."""
        text = "test"
        assert red(text) == color(text, "red")
        assert green(text) == color(text, "green")
        assert yellow(text) == color(text, "yellow")
        assert blue(text) == color(text, "blue")
        assert magenta(text) == color(text, "magenta")
        assert cyan(text) == color(text, "cyan")

    def test_color_with_invalid_name(self):
        """Test that invalid color names raise ValueError."""
        try:
            color("test", "invalid_color")  # type: ignore[arg-type]
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Unknown color" in str(e)

    def test_color_returns_text(self):
        """Test that color function returns text (possibly styled)."""
        result = color("test", "red")
        assert isinstance(result, str)
        assert "test" in result