# ruff: noqa: PLW0603
"""Theme system for CLI styling with CSS-like configuration."""

from typing import Any, Literal

from ruru.cli.styles import ColorName, color

ThemeName = Literal["default", "dark", "light", "minimal"]


class Theme:
    """A theme for CLI styling."""

    def __init__(self, name: str, colors: dict[str, ColorName], **kwargs: Any) -> None:
        """Initialize a theme.

        Args:
            name: Theme name.
            colors: Color mappings for different element types.
            **kwargs: Additional theme configuration.
        """
        self.name = name
        self.colors = colors
        self.config = kwargs

    def get_color(self, element_type: str) -> ColorName:
        """Get color for an element type.

        Args:
            element_type: Type of element (e.g., 'heading', 'error', 'success').

        Returns:
            Color name for the element type.
        """
        return self.colors.get(element_type, "white")

    def apply_color(self, text: str, element_type: str) -> str:
        """Apply theme color to text.

        Args:
            text: Text to color.
            element_type: Type of element.

        Returns:
            Colored text.
        """
        color_name = self.get_color(element_type)
        return color(text, color_name)


# Predefined themes
_THEMES: dict[ThemeName, Theme] = {
    "default": Theme(
        "default",
        {
            "heading": "bright_white",
            "subheading": "white",
            "success": "green",
            "error": "red",
            "warning": "yellow",
            "info": "blue",
            "dim": "bright_black",
        },
    ),
    "dark": Theme(
        "dark",
        {
            "heading": "bright_cyan",
            "subheading": "cyan",
            "success": "bright_green",
            "error": "bright_red",
            "warning": "bright_yellow",
            "info": "bright_blue",
            "dim": "bright_black",
        },
    ),
    "light": Theme(
        "light",
        {
            "heading": "black",
            "subheading": "bright_black",
            "success": "green",
            "error": "red",
            "warning": "yellow",
            "info": "blue",
            "dim": "bright_black",
        },
    ),
    "minimal": Theme(
        "minimal",
        {
            "heading": "white",
            "subheading": "white",
            "success": "white",
            "error": "white",
            "warning": "white",
            "info": "white",
            "dim": "bright_black",
        },
    ),
}


# Global theme state
_current_theme: Theme = _THEMES["default"]


def get_current_theme() -> Theme:
    """Get the currently active theme."""
    return _current_theme


def set_theme(theme: ThemeName | Theme) -> None:
    """Set the active theme.

    Args:
        theme: Theme name or Theme object.

    Raises:
        ValueError: If theme name is not recognized.
    """
    global _current_theme

    if isinstance(theme, Theme):
        _current_theme = theme
    elif theme in _THEMES:
        _current_theme = _THEMES[theme]
    else:
        available = ", ".join(_THEMES.keys())
        msg = f"Unknown theme: {theme}. Available themes: {available}"
        raise ValueError(msg)


def list_themes() -> list[str]:
    """List available theme names."""
    return list(_THEMES.keys())


def create_custom_theme(
    name: str, colors: dict[str, ColorName], **kwargs: Any
) -> Theme:
    """Create a custom theme.

    Args:
        name: Theme name.
        colors: Color mappings for element types.
        **kwargs: Additional theme configuration.

    Returns:
        New Theme object.
    """
    return Theme(name, colors, **kwargs)
