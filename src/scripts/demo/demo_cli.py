from ruru.cli import (
    alert,
    blue,
    bold,
    box,
    bullet_list,
    color,
    cyan,
    dim,
    green,
    heading,
    italic,
    magenta,
    numbered_list,
    paragraph,
    print_cli,
    red,
    rule,
    tree,
    underline,
    yellow,
)

# Section 1: Introduction
print_cli(rule())
print_cli(heading("CLI Elements & Styles Demo", level=1))
print_cli(paragraph("Demonstrates all core CLI elements and styles from ruru.cli."))
print_cli(rule())

# Section 2: Headings
for lvl in range(1, 7):
    print_cli(heading(f"Heading Level {lvl}", level=lvl))
print_cli(rule())

# Section 3: Alerts
for typ in ["info", "success", "warning", "error"]:
    print_cli(alert(f"This is an {typ} alert.", type=typ))
print_cli(rule())

# Section 4: Paragraph & Rule
sample_text = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
)
print_cli(paragraph(sample_text, width=50))
print_cli(rule(width=40))
print_cli(rule(width=40, char="="))
print_cli(rule())

# Section 5: Lists
items = ["Apple", "Banana", "Cherry"]
print_cli(bullet_list(items))
print_cli(numbered_list(items))
print_cli(rule())

# Section 6: Box & Tree
print_cli(box("This is a boxed message!", padding=2))
tree_items = ["Root", "Branch", "Leaf"]
print_cli(tree(tree_items))
print_cli(rule())

# Section 7: Styles
print_cli(bold("Bold text example"))
print_cli(dim("Dim text example"))
print_cli(italic("Italic text example"))
print_cli(underline("Underline text example"))
print_cli(rule())

# Section 8: Colors
print_cli(red("Red text"))
print_cli(green("Green text"))
print_cli(yellow("Yellow text"))
print_cli(blue("Blue text"))
print_cli(magenta("Magenta text"))
print_cli(cyan("Cyan text"))
print_cli(color("Bright yellow text", "bright_yellow"))
print_cli(rule())

# Section 9: Combined Example
combined = box(
    bullet_list(
        [
            bold("Bold item"),
            dim("Dim item"),
            italic("Italic item"),
            underline("Underline item"),
            red("Red item"),
            green("Green item"),
        ]
    ),
    padding=1,
)
print_cli(combined)
print_cli(rule())
