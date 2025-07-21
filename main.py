import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSlot

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

font_path = resource_path("MouldyCheeseRegular-WyMWG.ttf")
json_path = resource_path("buttons.json")

class ExpandableButton(QWidget):
    def __init__(self, label, description, parent):
        super().__init__()
        self.label = label
        self.description = description
        self.expanded = False
        self.parent = parent

        self.button = QPushButton(label)
        self.button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.button.setFixedHeight(40)  # Change button height here
        self.button.setFixedWidth(750)  # Change button width here (centered)  # Change button height here
        self.button.setStyleSheet("font-size: 16px; padding: 10px 15px 10px 15px; background-color: #444444; color: white; border-radius: 5px;")  # Change button text color, background, border-radius here  # Adjust button label padding: top, right, bottom, left  # Change button text font size here
        self.button.clicked.connect(self.toggle_description)

        self.desc_box = QTextEdit(description)
        self.desc_box.setStyleSheet("font-size: 14px; padding: 10px 15px 10px 15px; background-color: #333333; color: white; border: none;")  # Change expanded text color, background, border here  # Adjust expanded text padding: top, right, bottom, left  # Change description font size here
        self.desc_box.setReadOnly(True)
        self.desc_box.setMaximumHeight(0)
        self.desc_box.setFixedWidth(750)  # Change expanded text width here (centered)
        self.desc_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.desc_box.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.desc_box.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.animation = QPropertyAnimation(self.desc_box, b"maximumHeight")
        self.animation.setDuration(250)  # Adjust animation speed here (ms)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.finished.connect(self.cleanup_after_animation)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Center align everything in each button block
        layout.addWidget(self.button)
        layout.addWidget(self.desc_box)
        layout.setSpacing(5)
        self.setLayout(layout)

    @pyqtSlot()
    def toggle_description(self):
        if not self.expanded:
            self.parent.collapse_all_others(self)
        self.expanded = not self.expanded

        doc_height = self.desc_box.document().size().height() + 25  # Change buffer here if needed
        target_height = int(doc_height)

        if self.expanded:
            self.animation.setStartValue(self.desc_box.maximumHeight())
            self.animation.setEndValue(target_height)
        else:
            self.animation.setStartValue(self.desc_box.maximumHeight())
            self.animation.setEndValue(0)
        self.animation.start()

    @pyqtSlot()
    def cleanup_after_animation(self):
        self.desc_box.updateGeometry()
        self.updateGeometry()

    def collapse(self):
        if self.expanded:
            self.expanded = False
            self.animation.setStartValue(self.desc_box.maximumHeight())
            self.animation.setEndValue(0)
            self.animation.start()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expandable Buttons Example") # Change window title here
        self.setFixedSize(1000, 700)
        self.setStyleSheet("background-color: #1e1e1e;")  # Change main window background color here  # Change window size here

        headline = QLabel("Headline")
        headline.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px 20px 5px 20px; color: white;")  # Change headline text color here  # Adjust headline padding: top, right, bottom, left  # Change font size/weight here
        headline.setAlignment(Qt.AlignmentFlag.AlignCenter)

        intro_text = QLabel("Et totam earum ut soluta accusantium id veritatis recusandae nam voluptatem nescuint... (shortened for brevity)")  # Change placeholder text here
        intro_text.setStyleSheet("font-size: 13px; padding: 5px 50px 20px 50px; color: white;")  # Change intro text color here  # Adjust intro text padding: top, right, bottom, left  # Change intro text font size here  # Change placeholder text here
        intro_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        intro_text.setWordWrap(True)

        self.button_container = QVBoxLayout()
        self.button_container.setContentsMargins(20, 10, 20, 10)  # Adjust button container margins: left, top, right, bottom
        self.buttons = []

        # Container layout that includes headline, intro text, and buttons
        scroll_content_layout = QVBoxLayout()
        scroll_content_layout.addWidget(headline)
        scroll_content_layout.addWidget(intro_text)
        scroll_content_layout.addLayout(self.button_container)

        scroll_widget = QWidget()
        scroll_widget.setLayout(scroll_content_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)

        self.load_buttons()

    def load_buttons(self):
        json_path = resource_path("buttons.json")  # Update file name/path here if needed
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for entry in data:
            btn = ExpandableButton(entry["label"], entry["description"], self)
            self.buttons.append(btn)
            self.button_container.addWidget(btn)

    def collapse_all_others(self, current):
        for btn in self.buttons:
            if btn != current:
                btn.collapse()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load and apply custom font
    from PyQt6.QtGui import QFontDatabase, QFont
    font_id = QFontDatabase.addApplicationFont("MouldyCheeseRegular-WyMWG.ttf")  # Put your .ttf file in the same directory
    if font_id != -1:
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app_font = QFont(family, 10)  # 10 is base font size
        app.setFont(app_font)
    else:
        print("⚠️ Failed to load custom font. Make sure 'YourFont.ttf' is in the same folder.")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())