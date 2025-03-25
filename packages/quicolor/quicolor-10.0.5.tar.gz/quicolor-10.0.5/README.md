# Quicolor

Color formatting utility for Python console applications.

## Installation

```bash
pip install quicolor
```

## Usage

The package provides simple functions for adding color to your terminal output:

```python
import quicolor

# Basic color formatting
print(quicolor.red("This text will be red"))
print(quicolor.blue("This text will be blue"))
print(quicolor.green("This text will be green"))

# Text styles
print(quicolor.bold("Bold text"))
print(quicolor.underline("Underlined text"))
print(quicolor.italic("Italic text"))

# Combined formatting
print(quicolor.colorize("Custom formatting", 
                        color=quicolor.BLUE,
                        bg_color=quicolor.BG_WHITE,
                        style=quicolor.BOLD))

# Direct printing with color
quicolor.print_colored("This prints directly in magenta", quicolor.MAGENTA)

# Fun effects
print(quicolor.rainbow("Rainbow text!"))
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