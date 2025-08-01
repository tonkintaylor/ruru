"""Tests for CLI elements module."""

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


class TestHeading:
    def test_heading_basic(self):
        """Test basic heading creation."""
        result = heading("Test Heading")
        assert isinstance(result, str)
        assert "Test Heading" in result

    def test_heading_levels(self):
        """Test different heading levels."""
        text = "Test"
        for level in range(1, 7):
            result = heading(text, level=level)
            assert isinstance(result, str)
            assert text in result

    def test_heading_invalid_level(self):
        """Test that invalid heading levels raise ValueError."""
        try:
            heading("Test", level=0)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Heading level must be between 1 and 6" in str(e)

        try:
            heading("Test", level=7)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Heading level must be between 1 and 6" in str(e)


class TestAlert:
    def test_alert_basic(self):
        """Test basic alert creation."""
        result = alert("Test message")
        assert isinstance(result, str)
        assert "Test message" in result

    def test_alert_types(self):
        """Test different alert types."""
        message = "Test"
        for alert_type in ["info", "success", "warning", "error"]:
            result = alert(message, type=alert_type)  # type: ignore[arg-type]
            assert isinstance(result, str)
            assert message in result

    def test_alert_invalid_type(self):
        """Test that invalid alert types raise ValueError."""
        try:
            alert("Test", type="invalid")  # type: ignore[arg-type]
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Unknown alert type" in str(e)


class TestParagraph:
    def test_paragraph_basic(self):
        """Test basic paragraph creation."""
        text = "This is a test paragraph."
        result = paragraph(text)
        assert isinstance(result, str)
        assert text in result

    def test_paragraph_with_width(self):
        """Test paragraph with specified width."""
        text = "This is a very long text that should be wrapped when it exceeds the specified width."
        result = paragraph(text, width=20)
        assert isinstance(result, str)
        # Check that lines are not longer than specified width
        lines = result.split("\n")
        for line in lines:
            assert len(line) <= 20

    def test_paragraph_short_text(self):
        """Test paragraph with text shorter than width."""
        text = "Short text"
        result = paragraph(text, width=50)
        assert result == text


class TestRule:
    def test_rule_basic(self):
        """Test basic rule creation."""
        result = rule()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_rule_with_width(self):
        """Test rule with specified width."""
        width = 20
        result = rule(width=width)
        assert isinstance(result, str)
        assert len(result) == width

    def test_rule_with_custom_char(self):
        """Test rule with custom character."""
        char = "*"
        width = 10
        result = rule(width=width, char=char)
        assert result == char * width


class TestBulletList:
    def test_bullet_list_basic(self):
        """Test basic bullet list creation."""
        items = ["item1", "item2", "item3"]
        result = bullet_list(items)
        assert isinstance(result, str)
        for item in items:
            assert item in result

    def test_bullet_list_empty(self):
        """Test bullet list with empty items."""
        result = bullet_list([])
        assert result == ""

    def test_bullet_list_with_indent(self):
        """Test bullet list with custom indent."""
        items = ["item1"]
        result = bullet_list(items, indent=4)
        assert isinstance(result, str)
        assert result.startswith("    ")


class TestNumberedList:
    def test_numbered_list_basic(self):
        """Test basic numbered list creation."""
        items = ["item1", "item2", "item3"]
        result = numbered_list(items)
        assert isinstance(result, str)
        assert "1. item1" in result
        assert "2. item2" in result
        assert "3. item3" in result

    def test_numbered_list_empty(self):
        """Test numbered list with empty items."""
        result = numbered_list([])
        assert result == ""

    def test_numbered_list_with_indent(self):
        """Test numbered list with custom indent."""
        items = ["item1"]
        result = numbered_list(items, indent=4)
        assert isinstance(result, str)
        assert result.startswith("    1. item1")


class TestBox:
    def test_box_basic(self):
        """Test basic box creation."""
        content = "test content"
        result = box(content)
        assert isinstance(result, str)
        assert content in result
        assert "+" in result  # Should contain box corners
        assert "|" in result  # Should contain box sides

    def test_box_multiline(self):
        """Test box with multiline content."""
        content = "line1\nline2\nline3"
        result = box(content)
        assert isinstance(result, str)
        assert "line1" in result
        assert "line2" in result 
        assert "line3" in result

    def test_box_with_width(self):
        """Test box with specified width."""
        content = "test"
        width = 20
        result = box(content, width=width)
        assert isinstance(result, str)
        lines = result.split("\n")
        for line in lines:
            assert len(line) == width

    def test_box_with_padding(self):
        """Test box with custom padding."""
        content = "test"
        result = box(content, padding=2)
        assert isinstance(result, str)
        assert content in result


class TestTree:
    def test_tree_basic(self):
        """Test basic tree creation."""
        items = ["item1", "item2", "item3"]
        result = tree(items)
        assert isinstance(result, str)
        for item in items:
            assert item in result

    def test_tree_empty(self):
        """Test tree with empty items."""
        result = tree([])
        assert result == ""

    def test_tree_with_indent(self):
        """Test tree with custom indent."""
        items = ["item1", "item2"]
        result = tree(items, indent=4)
        assert isinstance(result, str)
        lines = result.split("\n")
        for line in lines:
            assert line.startswith("    ")  # 4 spaces