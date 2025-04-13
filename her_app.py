import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import Qt

class ExpandableButton(QWidget):
    def __init__(self, label, description):
        super().__init__()
        self.label = label
        self.description = description
        self.expanded = False

        self.button = QPushButton(label)
        self.button.clicked.connect(self.toggle_description)

        self.desc_box = QTextEdit(description)
        self.desc_box.setVisible(False)
        self.desc_box.setReadOnly(True)
        self.desc_box.setFixedHeight(120)
        self.desc_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.desc_box)
        self.setLayout(layout)

    def toggle_description(self):
        self.expanded = not self.expanded
        self.desc_box.setVisible(self.expanded)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expandable Buttons Example")
        self.setFixedSize(600, 800)  # Match your red margin area

        headline = QLabel("Headline")
        headline.setStyleSheet("font-size: 24px; font-weight: bold;")
        headline.setAlignment(Qt.AlignmentFlag.AlignCenter)

        intro_text = QLabel("""
        Et totam earum ut soluta accusantium id veritatis recusandae nam voluptatem nescuint... (shortened for brevity)
        """)
        intro_text.setWordWrap(True)

        self.button_container = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.button_container)
        scroll_area.setWidget(scroll_widget)

        layout = QVBoxLayout()
        layout.addWidget(headline)
        layout.addWidget(intro_text)
        layout.addWidget(scroll_area)

        self.setLayout(layout)

        self.load_buttons()

    def load_buttons(self):
        with open("buttons.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for entry in data:
            btn = ExpandableButton(entry["label"], entry["description"])
            self.button_container.addWidget(btn)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
