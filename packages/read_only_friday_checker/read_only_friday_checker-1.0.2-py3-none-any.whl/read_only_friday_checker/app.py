"""
This checks to see if today is Read Only Friday.
"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
)

from .rof_api_checker import RofApiChecker


class ReadOnlyFridayChecker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.show()

        # * Set window default settings
        self.setWindowTitle("Read Only Friday Checker")
        self.setFixedSize(300, 150)

        # * Create widgets
        self.rof_check = QPushButton("Is it read-only Friday? \nPress me to find out!")
        self.rof_check.setFixedSize(280, 130)
        self.rof_check.setFont(self.set_font())

        # * Create layout
        page = QVBoxLayout()
        page.addWidget(self.rof_check)

        gui = QWidget()
        gui.setLayout(page)

        self.setCentralWidget(gui)

        # * Define connections
        self.rof_check.pressed.connect(self.check_rof)

        # * Apply theme to window
        self.apply_theme()

    def check_rof(self):
        rof = RofApiChecker()
        (
            self.rof_check.setText("Yes! \nDon't change anything!")
            if rof.get_response().json()["readonly"] is True
            else self.rof_check.setText("Nope. \nChange away!")
        )

    def apply_theme(self):
        self.main_stylesheet = """
            background-color: #2e3440;
            color: #eceff4;
            border: 1px solid #434c5e;
            border-radius: 4px;
            padding: 2px 4px;
            """
        self.widget_stylesheet = """
            background-color: #4c566a;
            """
        self.setStyleSheet(self.main_stylesheet)
        self.rof_check.setStyleSheet(self.widget_stylesheet)

    def set_font(self):
        font = QFont()
        font.setPointSize(12)
        return font


def main():
    app = QApplication(sys.argv)
    main_window = ReadOnlyFridayChecker()  # noqa: F841
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
