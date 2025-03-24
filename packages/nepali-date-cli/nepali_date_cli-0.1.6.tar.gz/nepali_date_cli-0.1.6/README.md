# Nepali Date CLI

A simple command-line tool to display Nepali dates with Nepali numerals (देवनागरी अंक).

## Installation

You can install this package using pip:

```bash
pip install nepali-date-cli
```

To upgrade to the latest version:

```bash
pip install --upgrade nepali-date-cli
```

## Usage

### Command Line
After installation, you can use the `nepdate` command in your terminal:

```bash
nepdate
```

This will display both the current English date and the corresponding Nepali date with Nepali numerals.

### Python Code
You can also use it in your Python code:

```python
from nepali_date_cli import get_nepali_date

# Get today's date
nepali_date = get_nepali_date()
print(nepali_date)
```

## Example Output

```
English Date: Friday 2024-03-21
नेपाली मिति: शुक्रबार २०८०-१२-०८
```

## Features

- Displays current English date with day name
- Shows Nepali date in Devanagari numerals (देवनागरी अंक)
- Includes Nepali day names (e.g., आइतबार, सोमबार, etc.)
- Simple command-line interface
- Can be used as a Python module

## Requirements

- Python 3.6 or higher
- nepali-datetime package (automatically installed)

## License

This project is licensed under the MIT License. 