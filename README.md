<h1 align="center">
  <img width="237" height="92" alt="ruru" src="https://github.com/user-attachments/assets/499805bd-23f5-4868-9ec6-c2f1ba151203"><br>
</h1>

# ruru

[![PyPI Version](https://img.shields.io/pypi/v/ruru.svg)](<https://pypi.python.org/pypi/ruru>)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![usethis](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/usethis-python/usethis-python/main/assets/badge/v1.json)](https://github.com/usethis-python/usethis-python)

A collection of Python utilities ported from the R ecosystem.

## Features

### `config` module

The `ruru.config` module provides an equivalent utility to the [R `config` package](https://rstudio.github.io/config/articles/introduction.html), allowing for easy management of configuration settings in Python applications via YAML files. You can learn more about the module at <https://github.com/tonkintaylor/ruru/tree/develop/src/ruru/config.py> via the docstrings.

### `cli` module

The `ruru.cli` module provides a suite of tools to build attractive command line interfaces, inspired by the [R `cli` package](https://cran.r-project.org/web/packages/cli/index.html). It includes:

- **Semantic elements**: headings, alerts, paragraphs, lists, boxes, and rules
- **Text styling**: bold, italic, underline, dim, and colors
- **Unicode symbols** with ASCII fallbacks for compatibility
- **Themes**: CSS-like styling system with predefined themes (default, dark, light, minimal)
- **Smart terminal detection**: automatically adapts to terminal capabilities

#### Quick Example

```python
import ruru.cli as cli

# Headings and alerts
print(cli.heading("Welcome to My App", level=1))
print(cli.alert("Setup completed successfully!", type="success"))
print(cli.alert("Please review the configuration", type="warning"))

# Lists and formatting
items = ["Install dependencies", "Configure settings", "Run tests"]
print(cli.bullet_list(items))

# Boxes and rules
print(cli.box("Important: This is a highlighted message"))
print(cli.rule(width=50))

# Themes
cli.set_theme("dark")  # Switch to dark theme
print(cli.alert("Now using dark theme", type="info"))
```
