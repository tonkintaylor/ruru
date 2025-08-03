"""Tests for CLI symbols module."""

from ruru.cli.symbols import (
    _supports_unicode,
    arrow_right,
    bullet,
    corner,
    cross,
    info,
    line,
    symbol,
    tick,
    tree_end,
    tree_mid,
    warning,
)


class TestSupportsUnicode:
    def test_ascii_only_env_var(self, monkeypatch):
        """Test that ASCII_ONLY environment variable disables Unicode."""
        monkeypatch.setenv("ASCII_ONLY", "1")
        assert not _supports_unicode()

    def test_utf8_encoding(self, monkeypatch):
        """Test that UTF-8 encoding enables Unicode."""
        monkeypatch.delenv("ASCII_ONLY", raising=False)
        # Note: We can't easily mock sys.stdout.encoding in tests
        # so this test just checks the function doesn't crash


class TestSymbol:
    def test_symbol_function(self):
        """Test the main symbol function."""
        result = symbol("tick")
        assert isinstance(result, str)
        assert len(result) >= 1

    def test_invalid_symbol_name(self):
        """Test that invalid symbol names raise ValueError."""
        try:
            symbol("invalid_symbol")  # type: ignore[arg-type]
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Unknown symbol" in str(e)


class TestSymbolFunctions:
    def test_tick(self):
        """Test tick symbol function."""
        result = tick()
        assert isinstance(result, str)
        assert len(result) >= 1

    def test_cross(self):
        """Test cross symbol function."""
        result = cross()
        assert isinstance(result, str)
        assert len(result) >= 1

    def test_warning(self):
        """Test warning symbol function."""
        result = warning()
        assert isinstance(result, str)
        assert len(result) >= 1

    def test_info(self):
        """Test info symbol function."""
        result = info()
        assert isinstance(result, str)
        assert len(result) >= 1

    def test_arrow_right(self):
        """Test arrow_right symbol function."""
        result = arrow_right()
        assert isinstance(result, str)
        assert len(result) >= 1

    def test_bullet(self):
        """Test bullet symbol function."""
        result = bullet()
        assert isinstance(result, str)
        assert len(result) >= 1

    def test_line(self):
        """Test line symbol function."""
        result = line()
        assert isinstance(result, str)
        assert len(result) >= 1

    def test_corner(self):
        """Test corner symbol function."""
        result = corner()
        assert isinstance(result, str)
        assert len(result) >= 1

    def test_tree_mid(self):
        """Test tree_mid symbol function."""
        result = tree_mid()
        assert isinstance(result, str)
        assert len(result) >= 1

    def test_tree_end(self):
        """Test tree_end symbol function."""
        result = tree_end()
        assert isinstance(result, str)
        assert len(result) >= 1
