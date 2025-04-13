# Expandable Buttons UI

A simple Python + PyQt6 GUI that displays a headline, intro text, and expandable buttons that reveal additional content when clicked. Only one button can be expanded at a time, and both font sizes and layout styles are customizable.

## 🧩 Features

- Headline and intro paragraph
- Stackable buttons that expand on click
- Smooth slide animation using `QPropertyAnimation`
- Only one active/expanded button at a time
- All UI elements are centered and stylable
- Customizable:
  - Fonts, padding, colors
  - Button & expanded text width/height
  - Layout spacing and alignment

## 🛠 Tech Stack

- Python 3
- PyQt6
- JSON for dynamic button content

## 📁 File Structure

- `main.py` – core UI logic
- `buttons.json` – label + description data (editable)

## 🚀 Getting Started

```bash
pip install PyQt6
python main.py
```

## 📦 JSON Format

```json
[
  {
    "label": "Button 1",
    "description": "This is the content shown when Button 1 is expanded."
  },
  {
    "label": "Button 2",
    "description": "Another placeholder description."
  }
]
```

## ✏️ Customization

Open `main.py` and look for comments like:
- `# Change font size here`
- `# Adjust padding`
- `# Change color`

They’ll guide you on how to tweak the UI!

---

Created with ❤️ for clean, expandable interfaces.
