"""A suite of tools to build attractive command line interfaces.

Inspired by the R cli package (https://cran.r-project.org/web/packages/cli/index.html).

This module provides semantic elements like headings, lists, alerts, and paragraphs,
along with support for custom themes, ANSI colors, and Unicode symbols with ASCII
alternatives.
"""

from ruru.cli.elements import (
    alert,
    box,
    bullet_list,
    heading,
    numbered_list,
    paragraph,
    rule,
    tree,
)
from ruru.cli.styles import (
    bold,
    dim,
    italic,
    underline,
)
from ruru.cli.themes import (
    get_current_theme,
    list_themes,
    set_theme,
)

__all__ = [
    # Elements
    "alert",
    "box",
    "bullet_list",
    "heading", 
    "numbered_list",
    "paragraph",
    "rule",
    "tree",
    # Styles
    "bold",
    "dim",
    "italic",
    "underline",
    # Themes
    "get_current_theme",
    "list_themes", 
    "set_theme",
]