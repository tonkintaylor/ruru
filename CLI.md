# ruru CLI Module Overview

This document provides an overview of the CLI utilities in the `ruru` package, describing their organization, purpose, and usage.

## Module Structure

The CLI functionality is organized into four main modules:

- **elements.py**: Semantic building blocks for CLI output (headings, alerts, paragraphs, rules, lists, boxes, trees, print helper)
- **styles.py**: Text styling and color utilities (bold, dim, italic, underline, color functions)
- **themes.py**: Theme management for CLI color schemes (theme switching, listing, custom themes)
- **symbols.py**: Unicode/ASCII symbols for CLI (tick, cross, warning, info, arrows, bullets, lines, tree connectors)

## Module Details & Function List

### elements.py
Semantic CLI elements for structured output:
- `heading(text, level=1)`: Styled headings (levels 1-6)
- `alert(text, type="info")`: Alerts with symbol and color (info, success, warning, error)
- `paragraph(text, width=None)`: Paragraphs with optional word wrapping
- `rule(width=None, char=None)`: Horizontal rule lines
- `bullet_list(items, indent=2)`: Bulleted lists
- `numbered_list(items, indent=2)`: Numbered lists
- `box(content, width=None, padding=1)`: Text box around content
- `tree(items, indent=2)`: Tree structure display
- `print_cli(*args, **kwargs)`: Print helper for CLI output

### styles.py
Text styling and color utilities:
- `bold(text)`: Bold text
- `dim(text)`: Dim/faint text
- `italic(text)`: Italic text
- `underline(text)`: Underlined text
- `color(text, color_name)`: Apply color by name
- `red(text)`, `green(text)`, `yellow(text)`, `blue(text)`, `magenta(text)`, `cyan(text)`: Convenience color functions

### themes.py
Theme management for CLI color schemes:
- `get_current_theme()`: Get the active theme
- `set_theme(theme)`: Set the active theme (by name or Theme object)
- `list_themes()`: List available theme names
- `create_custom_theme(name, colors, **kwargs)`: Create a custom theme

### symbols.py
Unicode/ASCII symbols for CLI output:
- `symbol(name)`: Get symbol by name (tick, cross, warning, info, arrow_right, bullet, line, corner, tree_mid, tree_end)
- Convenience functions: `tick()`, `cross()`, `warning()`, `info()`, `arrow_right()`, `bullet()`, `line()`, `corner()`, `tree_mid()`, `tree_end()`

## Usage Example

Import CLI functions as needed:
```python
from ruru.cli import heading, alert, bold, box, bullet_list, rule
print(heading("Demo", level=1))
print(alert("Success!", type="success"))
print(box(bullet_list(["Item 1", "Item 2"])))
```

See `src/scripts/demo/demo_cli.py` for a full demonstration of all CLI elements and styles.
