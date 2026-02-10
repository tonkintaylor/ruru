import sys
from io import StringIO

import pytest

from ruru import cli


# Custom StringIO class with None encoding for testing
class StdoutWithNoneEncoding(StringIO):
    encoding = None  # type: ignore[assignment]


@pytest.mark.parametrize("heading_func", [cli.h1, cli.h2, cli.h3])
def test_heading_functions_produce_output(capfd, heading_func):
    """Test heading functions produce output."""
    heading_func("Test Heading")
    captured = capfd.readouterr()
    assert captured.out != ""


@pytest.mark.parametrize(
    ("alert_func", "msg"),
    [
        (cli.alert_success, "Success!"),
        (cli.alert_danger, "Danger!"),
        (cli.alert_warning, "Warning!"),
        (cli.alert_info, "Info!"),
        (cli.alert_note, "Note!"),
    ],
)
def test_alert_functions_produce_output(capfd, alert_func, msg):
    """Test alert functions produce output."""
    alert_func(msg)
    captured = capfd.readouterr()
    assert captured.out != ""


@pytest.mark.parametrize("items", [["Item 1", "Item 2", "Item 3"]])
def test_bullets_produce_output(capfd, items):
    """Test bullets function produces output."""
    cli.bullets(items)
    captured = capfd.readouterr()
    assert captured.out != ""


def test_bullets_with_dict(capfd):
    """Test bullets function with dict input."""
    input_dict = {
        "summary": "User requests a working example for D3.js tree components.",
        "category": "Code Request",
        "tags": ["HTML", "D3.js", "JavaScript", "Tree Component", "Data Visualization"],
    }
    cli.bullets(input_dict)
    captured = capfd.readouterr()
    expected_output = (
        "  • summary: User requests a working example for D3.js tree components.\n"
        "  • category: Code Request\n"
        "  • tags: HTML, D3.js, JavaScript, Tree Component, Data Visualization\n"
    )
    assert captured.out == expected_output


def test_bullets_with_mixed_types(capfd):
    """Test bullets function with mixed types in list."""
    mixed_list = ["Text item", 42, 3.14, True]
    cli.bullets(mixed_list)
    captured = capfd.readouterr()
    expected_output = "  • Text item\n  • 42\n  • 3.14\n  • True\n"
    assert captured.out == expected_output


def test_bullets_with_none_stdout_encoding(monkeypatch):
    """Test bullets handles None stdout.encoding gracefully."""
    mock_stdout = StdoutWithNoneEncoding()
    monkeypatch.setattr(sys, "stdout", mock_stdout)

    # Should not crash, should fall back to ASCII
    cli.bullets(["Item 1", "Item 2"])

    # Get the output
    output = mock_stdout.getvalue()
    assert "Item 1" in output
    assert "Item 2" in output
    assert "*" in output  # Should use ASCII bullet


def test_bullets_with_dict_none_stdout_encoding(monkeypatch):
    """Test bullets handles None stdout.encoding with dict input."""
    mock_stdout = StdoutWithNoneEncoding()
    monkeypatch.setattr(sys, "stdout", mock_stdout)

    # Should not crash
    stats = {
        "elapsed_seconds": 1.23,
        "input_tokens": 100,
        "output_tokens": 50,
    }
    cli.bullets(stats)

    # Get the output
    output = mock_stdout.getvalue()
    assert "elapsed_seconds" in output
    assert "*" in output  # Should use ASCII bullet
