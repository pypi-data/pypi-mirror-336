# quickcolors

Color formatting utility for Python console applications.

## Installation

```bash
pip install quickcolors
```

## Usage

The package provides simple functions for adding color to your terminal output:

```python
import quickcolors

# Basic color formatting
print(quickcolors.red("This text will be red"))
print(quickcolors.blue("This text will be blue"))
print(quickcolors.green("This text will be green"))

# Text styles
print(quickcolors.bold("Bold text"))
print(quickcolors.underline("Underlined text"))
print(quickcolors.italic("Italic text"))

# Combined formatting
print(quickcolors.colorize("Custom formatting", 
                        color=quickcolors.BLUE,
                        bg_color=quickcolors.BG_WHITE,
                        style=quickcolors.BOLD))

# Direct printing with color
quickcolors.print_colored("This prints directly in magenta", quickcolors.MAGENTA)

# Fun effects
print(quickcolors.rainbow("Rainbow text!"))
```

## Available Functions

### Colors
- `black(text)`
- `red(text)`
- `green(text)`
- `yellow(text)`
- `blue(text)`
- `magenta(text)`
- `cyan(text)`
- `white(text)`

### Text Styles
- `bold(text)`
- `italic(text)`
- `underline(text)`

### Background Highlighting
- `highlight(text, bg_color=BG_YELLOW)`

### Utilities
- `colorize(text, color, bg_color, style)` - For custom combinations
- `print_colored(text, color, bg_color, style)` - Print with colors
- `rainbow(text)` - Creates rainbow-colored text
- `is_colored_terminal()` - Check if terminal supports colors

## Color Constants

You can use these constants for custom formatting:

### Text Colors
`BLACK`, `RED`, `GREEN`, `YELLOW`, `BLUE`, `MAGENTA`, `CYAN`, `WHITE`, `RESET`

### Background Colors
`BG_BLACK`, `BG_RED`, `BG_GREEN`, `BG_YELLOW`, `BG_BLUE`, `BG_MAGENTA`, `BG_CYAN`, `BG_WHITE`

### Text Styles
`BOLD`, `UNDERLINE`, `ITALIC`

## Note

This package is designed for Windows systems, but works on any platform that supports ANSI color codes. 