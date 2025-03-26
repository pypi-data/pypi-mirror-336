![Banner Termpyx](image.png)

# TermPyx

**Beautiful and Animated Terminal Logging for Python** 🐍✨

[![PyPI Version](https://img.shields.io/pypi/v/termpyx.svg)](https://pypi.org/project/termpyx/)
[![License](https://img.shields.io/github/license/techatlasdev/termpyx)](https://github.com/techatlasdev/termpyx/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/termpyx.svg)](https://pypi.org/project/termpyx/)

---

## 🌟 Overview

TermPyx is a Python library designed to enhance terminal logging with colors and animations. It provides an intuitive interface for displaying various log levels, including success, info, warning, danger, and debug messages, all with customizable colors and optional animated text output.

---

## 🚀 Features

- **🎨 Colored Logging**: Easily distinguish log messages with customizable colors.
- **🎬 Animated Output**: Optional animated text display for dynamic terminal feedback.
- **📝 Multiple Log Levels**: Support for success, info, warning, danger, and debug messages.
- **📏 Section Separators**: Create visually distinct sections in your terminal output.
- **🐞 Debug Mode**: Toggle debug messages on or off as needed.

---

## 🛠️ Installation

Install TermPyx using pip:

```bash
pip install termpyx
```

---

## 📖 Usage

Here's how to get started with TermPyx:

```python
from termpyx import Console

# Initialize the console with animation and debug mode enabled
console = Console(animated=True, in_debug=True)

# Standard log message
console.log("Processing data...")

# Success message
console.success("Operation completed successfully!")

# Info message
console.info("This is an informational message.")

# Warning message
console.warning("This is a warning message.")

# Danger/Error message
console.danger("An error has occurred!")

# Debug message (only displayed if in_debug is True)
console.debug("Debugging details here.")

# Error message
console.error("An error has been ocurred.")

# Section separator
console.separator("Section 1")
```

---

## 🎨 Customization

You can customize the colors of different log levels by modifying the `Console` class attributes:

```python
from termpyx import Console, Color

console = Console()
console.cLog = Color.CYAN
console.cSuccess = Color.MAGENTA
# ... and so on for other log levels
```

---

## 🐞 Debug Mode

To enable or disable debug messages:

```python
console = Console(in_debug=True)  # Debug messages will be shown
console = Console(in_debug=False) # Debug messages will be hidden
```

---

## 🎬 Animated Output

Enable animated text output by setting the `animated` parameter to `True`:

```python
console = Console(animated=True)
```

---

## 🛡️ License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/techatlasdev/termpyx/blob/main/LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

---

## 📞 Contact

For any questions or inquiries, please open an issue on the [GitHub repository](https://github.com/techatlasdev/termpyx/issues).

---

*Elevate your terminal logging experience with TermPyx!*
