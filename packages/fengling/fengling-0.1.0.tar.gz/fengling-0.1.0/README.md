# Fengling Progress

A beautiful progress bar library with various emoji styles including fruits, windchimes, and dynamic animations.

## Installation

```bash
pip install fengling
```

## Usage

```python
from fengling import WindchimeProgress

# Create a progress bar with default style (windchime)
progress = WindchimeProgress(total=100)

# Update progress
for i in range(100):
    progress.update(i + 1)
    # Do your work here
    time.sleep(0.1)

# Complete the progress bar
progress.finish()
```

## Available Styles

### Fruit Styles
- 🍎 Red Apple (ala)
- 🫐 Blueberry
- 🍏 Green Apple
- 🍊 Orange
- 🍇 Grape
- 🍓 Strawberry
- 🍑 Peach
- 🍐 Pear
- 🍌 Banana
- 🍉 Watermelon

### Decorative Styles
- 🎐 Windchime (default)
- 🔔 Bell
- 🎋 Chime
- ⛩️ Temple
- 🎀 Ribbon
- ✨ Sparkle
- ⭐ Star
- 💎 Crystal

### Dynamic Styles
- 🏃 Running
- 🚶 Walking
- 🚶‍♂️ Strolling
- 🚀 Rocket

## Examples

```python
from fengling import WindchimeProgress
import time

# Show all available styles
WindchimeProgress.show_styles()

# Create a progress bar with specific style
progress = WindchimeProgress(total=100, style='ala')  # Red apple style
for i in range(100):
    progress.update(i + 1)
    time.sleep(0.1)
progress.finish()

# Try different styles
progress = WindchimeProgress(total=100, style='rocket')  # Rocket style
for i in range(100):
    progress.update(i + 1)
    time.sleep(0.1)
progress.finish()
```

## Features

- Beautiful emoji animations
- Multiple style options
- Color-coded progress bars
- Simple and intuitive API
- Customizable progress bar length
- Support for percentage display
- Elapsed time tracking

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 