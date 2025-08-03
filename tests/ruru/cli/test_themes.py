"""Tests for CLI themes module."""

from ruru.cli.themes import (
    Theme,
    create_custom_theme,
    get_current_theme,
    list_themes,
    set_theme,
)


class TestTheme:
    def test_theme_creation(self):
        """Test basic theme creation."""
        colors = {"heading": "red", "error": "blue"}
        theme = Theme("test", colors)
        assert theme.name == "test"
        assert theme.colors == colors

    def test_theme_get_color(self):
        """Test getting colors from theme."""
        colors = {"heading": "red", "error": "blue"}
        theme = Theme("test", colors)
        assert theme.get_color("heading") == "red"
        assert theme.get_color("error") == "blue"
        assert theme.get_color("unknown") == "white"  # Default

    def test_theme_apply_color(self):
        """Test applying theme colors to text."""
        colors = {"heading": "red"}
        theme = Theme("test", colors)
        result = theme.apply_color("test", "heading")
        assert isinstance(result, str)
        assert "test" in result


class TestThemeManagement:
    def test_get_current_theme(self):
        """Test getting current theme."""
        theme = get_current_theme()
        assert isinstance(theme, Theme)

    def test_list_themes(self):
        """Test listing available themes."""
        themes = list_themes()
        assert isinstance(themes, list)
        assert len(themes) > 0
        assert "default" in themes
        assert "dark" in themes
        assert "light" in themes
        assert "minimal" in themes

    def test_set_theme_by_name(self):
        """Test setting theme by name."""
        original = get_current_theme()

        # Set to dark theme
        set_theme("dark")
        current = get_current_theme()
        assert current.name == "dark"

        # Reset to original
        set_theme(original)

    def test_set_theme_by_object(self):
        """Test setting theme by Theme object."""
        original = get_current_theme()

        # Create custom theme
        custom = create_custom_theme("custom", {"heading": "cyan"})
        set_theme(custom)
        current = get_current_theme()
        assert current.name == "custom"

        # Reset to original
        set_theme(original)

    def test_set_theme_invalid_name(self):
        """Test setting theme with invalid name."""
        try:
            set_theme("invalid_theme")  # type: ignore[arg-type]
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Unknown theme" in str(e)


class TestCustomThemes:
    def test_create_custom_theme(self):
        """Test creating custom themes."""
        colors = {"heading": "cyan", "error": "magenta"}
        theme = create_custom_theme("custom", colors, extra_config="value")
        assert theme.name == "custom"
        assert theme.colors == colors
        assert theme.config["extra_config"] == "value"
