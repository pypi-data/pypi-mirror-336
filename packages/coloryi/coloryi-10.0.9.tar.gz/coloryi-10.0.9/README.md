# coloris

Color formatting utility for Python console applications.

## Installation

```bash
pip install coloris
```

## Usage

The package provides simple functions for adding color to your terminal output:

```python
import coloris

# Basic color formatting
print(coloris.red("This text will be red"))
print(coloris.blue("This text will be blue"))
print(coloris.green("This text will be green"))

# Text styles
print(coloris.bold("Bold text"))
print(coloris.underline("Underlined text"))
print(coloris.italic("Italic text"))

# Combined formatting
print(coloris.colorize("Custom formatting", 
                        color=coloris.BLUE,
                        bg_color=coloris.BG_WHITE,
                        style=coloris.BOLD))

# Direct printing with color
coloris.print_colored("This prints directly in magenta", coloris.MAGENTA)

# Fun effects
print(coloris.rainbow("Rainbow text!"))
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