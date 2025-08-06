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

### `base` module

The `ruru.base` module provides utilities for argument matching:

- `match_arg`: A Python equivalent of R's [`match.arg`](https://www.rdocumentation.org/packages/base/versions/3.6.2/topics/match.arg) function for verifying function arguments against a set of valid options.

Inspired by the R [`config`](https://rstudio.github.io/config/articles/introduction.html/) package.

### `config` module

The `ruru.config` module gives an easy way to manage of configuration settings in Python applications via YAML files.

```python
from importlib.resources import files
from ruru.config import get as get_config

config_path = files("ruru.cli").joinpath("config.yml") 
config = get_config(file = config_path)
```

Inspired by the R [`config`](https://rstudio.github.io/config/articles/introduction.html/) package.

### `cli` module

The `ruru.cli` module provides utilities for enhanced command-line interface output, including colored text, formatted headings, alert messages, and bullet-point lists.

Recommended usage:

```python
from ruru import cli
cli.h1("Heading")
cli.alert("This is an alert message")
```

Inspired by the R [`cli`](https://cli.r-lib.org/reference/index.html) package.
