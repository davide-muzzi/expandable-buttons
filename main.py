import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSlot

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
        self.button.setStyleSheet("font-size: 16px;")  # Change button text font size here
        self.button.clicked.connect(self.toggle_description)

        self.desc_box = QTextEdit(description)
        self.desc_box.setStyleSheet("font-size: 14px;")  # Change description font size here
        self.desc_box.setReadOnly(True)
        self.desc_box.setMaximumHeight(0)
        self.desc_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.desc_box.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.desc_box.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.animation = QPropertyAnimation(self.desc_box, b"maximumHeight")
        self.animation.setDuration(250)  # Adjust animation speed here (ms)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.finished.connect(self.cleanup_after_animation)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.desc_box)
        layout.setSpacing(5)
        self.setLayout(layout)

    @pyqtSlot()
    def toggle_description(self):
        if not self.expanded:
            self.parent.collapse_all_others(self)
        self.expanded = not self.expanded

        doc_height = self.desc_box.document().size().height() + 10  # Change buffer here if needed
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
        self.setWindowTitle("Expandable Buttons Example")
        self.setFixedSize(1000, 700)  # Change window size here

        headline = QLabel("Headline")
        headline.setStyleSheet("font-size: 24px; font-weight: bold;")  # Change font size/weight here
        headline.setAlignment(Qt.AlignmentFlag.AlignCenter)

        intro_text = QLabel("Et totam earum ut soluta accusantium id veritatis recusandae nam voluptatum nesciunt et beatae officia. Quo numquam quam aut officiis possimus et dolores voluptatem et amet molestiae est itaque deserunt sed tenetur atque 33 fugit similique. Qui sunt voluptatem non dolorem quidem qui dolor nihil ut accusantium voluptas quo atque vero aut similique voluptas!Eum labore deserunt ut odit voluptate et distinctio tempora qui autem magni eum dicta delectus aut esse galisum. Quo quae eligendi ea aliquid nihil et neque enim At voluptatum consequuntur quo odit rerum et laboriosam ducimus? Lorem ipsum dolor sit amet. Ex vitae dolor et voluptatem veniam rem quia animi et maxime voluptatem aut tenetur ipsam eos voluptas enim eos alias velit. Eum quos voluptatem et fuga saepe sed incidunt odio aut inventore impedit et voluptates ducimus! Et corporis delectus sit quidem aliquam est quam sint aut deleniti possimus est impedit perferendis hic assumenda dolor est excepturi nobis.")  # Change placeholder text here
        intro_text.setStyleSheet("font-size: 13px;")  # Change intro text font size here  # Change placeholder text here
        intro_text.setWordWrap(True)

        self.button_container = QVBoxLayout()
        self.buttons = []

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
        json_path = os.path.join(os.path.dirname(__file__), "buttons.json")  # Update file name/path here if needed
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
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
