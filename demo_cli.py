#!/usr/bin/env python3
"""Demo script showcasing ruru CLI functionality."""

import os

import ruru.cli as cli


def main():
    """Demo the CLI functionality."""
    print("=" * 60)
    print(cli.heading("🎨 RURU CLI Demo", level=1))
    print("=" * 60)
    print()
    
    # Headings demo
    print(cli.heading("📝 Headings", level=2))
    for level in range(1, 7):
        print(cli.heading(f"Heading Level {level}", level=level))
    print()
    
    # Alerts demo
    print(cli.heading("🚨 Alerts", level=2))
    print(cli.alert("This is an informational message"))
    print(cli.alert("Operation completed successfully!", type="success"))
    print(cli.alert("Please review this carefully", type="warning"))
    print(cli.alert("Something went wrong!", type="error"))
    print()
    
    # Text styling demo
    print(cli.heading("🎭 Text Styling", level=2))
    print(f"Normal text")
    print(f"This is {cli.bold('bold')} text")
    print(f"This is {cli.italic('italic')} text")
    print(f"This is {cli.underline('underlined')} text")
    print(f"This is {cli.dim('dimmed')} text")
    print()
    
    # Colors demo
    print(cli.heading("🌈 Colors", level=2))
    from ruru.cli.styles import red, green, yellow, blue, magenta, cyan
    print(f"Colors: {red('red')} {green('green')} {yellow('yellow')} {blue('blue')} {magenta('magenta')} {cyan('cyan')}")
    print()
    
    # Paragraph demo
    print(cli.heading("📄 Paragraphs", level=2))
    long_text = ("This is a demonstration of paragraph wrapping functionality. "
                 "The text will automatically wrap to fit within the specified "
                 "width, making it easier to read in terminal environments. "
                 "This is particularly useful for creating readable CLI help "
                 "text and documentation.")
    print(cli.paragraph(long_text, width=50))
    print()
    
    # Rules demo
    print(cli.heading("📏 Rules", level=2))
    print("Thin rule:")
    print(cli.rule(width=40))
    print("Custom character rule:")
    print(cli.rule(width=40, char="="))
    print("Thick rule:")
    print(cli.rule(width=40, char="█"))
    print()
    
    # Lists demo
    print(cli.heading("📋 Lists", level=2))
    items = ["First item", "Second item", "Third item with longer text"]
    print("Bullet list:")
    print(cli.bullet_list(items))
    print("\nNumbered list:")
    print(cli.numbered_list(items))
    print()
    
    # Box demo
    print(cli.heading("📦 Boxes", level=2))
    box_content = "This is content\ninside a box\nwith multiple lines"
    print(cli.box(box_content))
    print()
    
    # Themes demo
    print(cli.heading("🎨 Themes", level=2))
    print(f"Available themes: {', '.join(cli.list_themes())}")
    print("\nDefault theme:")
    print(cli.alert("Default theme message", type="info"))
    
    cli.set_theme("dark")
    print("Dark theme:")
    print(cli.alert("Dark theme message", type="success"))
    
    cli.set_theme("minimal")
    print("Minimal theme:")
    print(cli.alert("Minimal theme message", type="warning"))
    
    # Reset to default
    cli.set_theme("default")
    print()
    
    # Tree demo
    print(cli.heading("🌳 Trees", level=2))
    tree_items = ["Root", "Branch 1", "Branch 2", "Leaf"]
    print(cli.tree(tree_items))
    print()
    
    # Symbol fallback demo
    print(cli.heading("🔣 Symbol Fallbacks", level=2))
    print("Unicode mode:")
    from ruru.cli.symbols import tick, cross, warning, info, arrow_right, bullet
    print(f"  {tick()} {cross()} {warning()} {info()} {arrow_right()} {bullet()}")
    
    # Force ASCII mode for demo
    original_ascii = os.environ.get("ASCII_ONLY")
    os.environ["ASCII_ONLY"] = "1"
    print("ASCII mode (ASCII_ONLY=1):")
    print(f"  {tick()} {cross()} {warning()} {info()} {arrow_right()} {bullet()}")
    
    # Restore original setting
    if original_ascii is None:
        os.environ.pop("ASCII_ONLY", None)
    else:
        os.environ["ASCII_ONLY"] = original_ascii
    
    print()
    print(cli.rule(width=60))
    print(cli.alert("Demo completed! 🎉", type="success"))


if __name__ == "__main__":
    main()