"""Semantic CLI elements like headings, alerts, paragraphs, and rules."""

import sys
from typing import Literal

from ruru.cli.styles import bold, color, dim
from ruru.cli.symbols import cross, info, line, tick, warning, bullet, tree_mid, tree_end
from ruru.cli.themes import get_current_theme


AlertType = Literal["info", "success", "warning", "error"]


def heading(text: str, *, level: int = 1) -> str:
    """Create a styled heading.
    
    Args:
        text: The heading text.
        level: Heading level (1-6, similar to HTML h1-h6).
        
    Returns:
        Formatted heading string.
    """
    if not 1 <= level <= 6:
        msg = "Heading level must be between 1 and 6"
        raise ValueError(msg)
    
    theme = get_current_theme()
    
    # Style based on level
    if level == 1:
        return bold(theme.apply_color(text, "heading"))
    elif level == 2:
        return bold(theme.apply_color(text, "subheading"))
    elif level == 3:
        return theme.apply_color(text, "heading")
    elif level == 4:
        return theme.apply_color(text, "subheading")
    elif level == 5:
        return dim(theme.apply_color(text, "subheading"))
    else:  # level == 6
        return dim(text)


def alert(text: str, *, type: AlertType = "info") -> str:
    """Create a styled alert message.
    
    Args:
        text: The alert message text.
        type: Type of alert (info, success, warning, error).
        
    Returns:
        Formatted alert string with appropriate symbol and color.
    """
    symbol_map = {
        "info": (info(), "info"),
        "success": (tick(), "success"), 
        "warning": (warning(), "warning"),
        "error": (cross(), "error"),
    }
    
    if type not in symbol_map:
        msg = f"Unknown alert type: {type}"
        raise ValueError(msg)
    
    symbol_char, theme_key = symbol_map[type]
    theme = get_current_theme()
    colored_symbol = theme.apply_color(symbol_char, theme_key)
    
    return f"{colored_symbol} {text}"


def paragraph(text: str, *, width: int | None = None) -> str:
    """Create a formatted paragraph with optional text wrapping.
    
    Args:
        text: The paragraph text.
        width: Maximum line width for text wrapping. If None, uses terminal width.
        
    Returns:
        Formatted paragraph string.
    """
    if width is None:
        # Try to get terminal width, fallback to 80
        try:
            import shutil
            width = shutil.get_terminal_size().columns
        except (ImportError, OSError):
            width = 80
    
    # Simple word wrapping
    if len(text) <= width:
        return text
    
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + len(current_line) <= width:
            current_line.append(word)
            current_length += len(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(" ".join(current_line))
    
    return "\n".join(lines)


def rule(*, width: int | None = None, char: str | None = None) -> str:
    """Create a horizontal rule line.
    
    Args:
        width: Width of the rule. If None, uses terminal width.
        char: Character to use for the rule. If None, uses line symbol.
        
    Returns:
        Formatted rule string.
    """
    if width is None:
        # Try to get terminal width, fallback to 80
        try:
            import shutil
            width = shutil.get_terminal_size().columns
        except (ImportError, OSError):
            width = 80
    
    if char is None:
        char = line()
    
    return char * width


def print_cli(*args, **kwargs) -> None:
    """Print CLI elements to stdout.
    
    This is a convenience function that wraps the standard print function
    but can be used consistently with other CLI elements.
    """
    print(*args, **kwargs, file=sys.stdout)


def bullet_list(items: list[str], *, indent: int = 2) -> str:
    """Create a bulleted list.
    
    Args:
        items: List of items to display.
        indent: Number of spaces to indent each item.
        
    Returns:
        Formatted list string.
    """
    if not items:
        return ""
    
    bullet_char = bullet()
    indent_str = " " * indent
    
    lines = []
    for item in items:
        lines.append(f"{indent_str}{bullet_char} {item}")
    
    return "\n".join(lines)


def numbered_list(items: list[str], *, indent: int = 2) -> str:
    """Create a numbered list.
    
    Args:
        items: List of items to display.
        indent: Number of spaces to indent each item.
        
    Returns:
        Formatted list string.
    """
    if not items:
        return ""
    
    indent_str = " " * indent
    
    lines = []
    for i, item in enumerate(items, 1):
        lines.append(f"{indent_str}{i}. {item}")
    
    return "\n".join(lines)


def box(content: str, *, width: int | None = None, padding: int = 1) -> str:
    """Create a text box around content.
    
    Args:
        content: Content to put in the box.
        width: Box width. If None, uses content width plus padding.
        padding: Padding around content.
        
    Returns:
        Formatted box string.
    """
    lines = content.strip().split("\n")
    
    if width is None:
        max_line_length = max(len(line) for line in lines) if lines else 0
        width = max_line_length + 2 * padding + 2  # +2 for borders
    
    # Use simple ASCII characters for the box
    horizontal = "-"
    vertical = "|"
    corner = "+"
    
    # Calculate content width
    content_width = width - 2  # Subtract borders
    
    # Create box
    top_border = corner + horizontal * (width - 2) + corner
    bottom_border = top_border
    
    box_lines = [top_border]
    
    for line in lines:
        # Pad or truncate line to fit content width
        padded_line = line.ljust(content_width - 2 * padding)[:content_width - 2 * padding]
        
        # Add padding and borders
        padding_str = " " * padding
        box_line = vertical + padding_str + padded_line + padding_str + vertical
        box_lines.append(box_line)
    
    box_lines.append(bottom_border)
    
    return "\n".join(box_lines)


def tree(items: list[str], *, indent: int = 2) -> str:
    """Create a tree structure display.
    
    Args:
        items: List of items to display in tree format.
        indent: Number of spaces for indentation.
        
    Returns:
        Formatted tree string.
    """
    if not items:
        return ""
    
    lines = []
    indent_str = " " * indent
    
    for i, item in enumerate(items):
        if i == len(items) - 1:
            # Last item
            connector = tree_end()
            lines.append(f"{indent_str}{connector} {item}")
        else:
            # Not last item
            connector = tree_mid()
            lines.append(f"{indent_str}{connector} {item}")
    
    return "\n".join(lines)