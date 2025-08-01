"""Tests for the CLI module."""

from ruru.cli import (
    alert,
    bold,
    box,
    bullet_list,
    dim,
    get_current_theme,
    heading,
    italic,
    list_themes,
    numbered_list,
    paragraph,
    rule,
    set_theme,
    underline,
)


class TestCLIImports:
    def test_imports_work(self):
        """Test that all public CLI functions can be imported and called."""
        # Test elements
        assert callable(alert)
        assert callable(box)
        assert callable(bullet_list)
        assert callable(heading)
        assert callable(numbered_list)
        assert callable(paragraph)
        assert callable(rule)
        
        # Test styles
        assert callable(bold)
        assert callable(dim)
        assert callable(italic)
        assert callable(underline)
        
        # Test themes
        assert callable(get_current_theme)
        assert callable(list_themes)
        assert callable(set_theme)

    def test_basic_functionality(self):
        """Test basic functionality of imported functions."""
        # Test that functions return strings
        assert isinstance(heading("Test"), str)
        assert isinstance(alert("Test"), str)
        assert isinstance(box("Test"), str)
        assert isinstance(bullet_list(["Test"]), str)
        assert isinstance(numbered_list(["Test"]), str)
        assert isinstance(paragraph("Test"), str)
        assert isinstance(rule(width=10), str)
        assert isinstance(bold("Test"), str)
        assert isinstance(dim("Test"), str)
        assert isinstance(italic("Test"), str)
        assert isinstance(underline("Test"), str)
        
        # Test theme functions
        assert isinstance(get_current_theme().name, str)
        assert isinstance(list_themes(), list)