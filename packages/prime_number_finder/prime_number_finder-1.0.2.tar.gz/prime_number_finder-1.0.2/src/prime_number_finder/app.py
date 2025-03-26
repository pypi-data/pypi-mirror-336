"""
Python program for finding/checking Prime Numbers.
"""

import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
)

from .prime_checker import PrimeChecker
from .yaml_file_handler import YamlFileHandler
from .prime_file_handler import PrimeFileHandler

config_file = YamlFileHandler("resources/configs/config.yml")
config = config_file.load_yaml_file()

themes_file = YamlFileHandler("resources/configs/themes.yml")
themes = themes_file.load_yaml_file()


class PrimeNumberFinder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.show()

        # * Set window default settings
        self.setWindowTitle(config["window_settings"]["title"])
        self.setMaximumSize(
            config["window_settings"]["min_width"],
            config["window_settings"]["min_height"],
        )

        # * Define normal variables
        self.prime_file_handler = PrimeFileHandler()
        self.current_number = self.prime_file_handler.load_current_number()
        self.check_number = int()
        self.prime_list = self.prime_file_handler.load_prime_numbers()
        self.prime_checker = PrimeChecker(self.prime_list)
        self.keep_iterating = False

        # * Create widgets and apply settings to them
        self.iterate_button = QPushButton("Iterate")

        self.iterate_timer = QTimer(self)
        self.iterate_timer.setInterval(10)

        self.most_recent_number_text = QLabel(
            "Most recent number checked: ", alignment=Qt.AlignmentFlag.AlignLeft
        )
        self.most_recent_number = QLabel(
            str(self.current_number), alignment=Qt.AlignmentFlag.AlignRight
        )

        self.most_recent_prime_text = QLabel(
            "Most recent prime found: ", alignment=Qt.AlignmentFlag.AlignLeft
        )
        self.most_recent_prime = QLabel(
            str(self.prime_list[-1]), alignment=Qt.AlignmentFlag.AlignRight
        )

        self.check_button = QPushButton("Check for Primality")

        self.check_input = QLineEdit(f"{self.current_number}")
        self.check_input.setValidator(QIntValidator(bottom=0))

        self.check_output = QLabel()

        self.check_timer = QTimer(self)
        self.check_timer.setInterval(10)

        self.theme_toggle = QPushButton("Dark")

        self.check_click()

        # * Define button connections
        self.iterate_button.pressed.connect(self.iterate_click)
        self.iterate_timer.timeout.connect(self.iterate)
        self.check_button.pressed.connect(self.check_click)
        self.check_timer.timeout.connect(self.check_iterate)

        # * Create layouts
        page = QVBoxLayout()
        row_one = QHBoxLayout()
        row_two = QHBoxLayout()
        row_three = QHBoxLayout()
        row_four = QHBoxLayout()

        # * Add widgets to layouts
        row_one.addWidget(self.iterate_button)

        row_two.addWidget(self.most_recent_number_text)
        row_two.addWidget(self.most_recent_number)

        row_three.addWidget(self.most_recent_prime_text)
        row_three.addWidget(self.most_recent_prime)

        row_four.addWidget(self.check_button)
        row_four.addWidget(self.check_input)
        row_four.addWidget(self.check_output)

        # * Setup overall page layout and set default window theme
        page.addLayout(row_one)
        page.addLayout(row_two)
        page.addLayout(row_three)
        page.addLayout(row_four)

        gui = QWidget()
        gui.setLayout(page)

        self.setCentralWidget(gui)

        self.apply_theme(self.theme_toggle.text().lower())

    def iterate_click(self):
        self.keep_iterating = not self.keep_iterating
        if self.keep_iterating:
            self.iterate_button.setText("Stop Iterating")
            self.iterate_timer.start()
        else:
            self.iterate_button.setText("Iterate")
            self.iterate_timer.stop()

    def iterate(self):
        if self.keep_iterating:
            is_prime = self.prime_checker.prime_check(self.current_number)

            if is_prime is True:
                self.prime_file_handler.save_found_prime(self.current_number)
                self.prime_list.append(self.current_number)
                self.most_recent_prime.setText(str(self.current_number))

            self.current_number += 1
            self.prime_file_handler.save_current_number(self.current_number)
            self.most_recent_number.setText(str(self.current_number))

    def check_click(self):
        self.check_number = int(self.check_input.text())
        self.check_button.setText("Checking")

        if self.check_number <= self.current_number:
            if self.check_number in self.prime_list:
                self.check_output.setText("is prime!")
            else:
                self.check_output.setText("is not prime!")
            self.check_button.setText("Check for Primality")
            self.check_timer.stop()
        else:
            self.check_timer.start()

    def check_iterate(self):
        if self.check_number > self.current_number:
            is_prime = self.prime_checker.prime_check(self.current_number)

            if is_prime is True:
                self.prime_file_handler.save_found_prime(self.current_number)
                self.prime_list.append(self.current_number)
                self.most_recent_prime.setText(str(self.current_number))

            self.current_number += 1
            self.prime_file_handler.save_current_number(self.current_number)
            self.most_recent_number.setText(str(self.current_number))

        self.check_click()

    def toggle_theme(self):
        if self.theme_toggle.text() == "Dark":
            self.theme_toggle.setText("Light")
            theme = self.theme_toggle.text()
        else:
            self.theme_toggle.setText("Dark")
            theme = self.theme_toggle.text()

        self.apply_theme(theme.lower())

    def apply_theme(self, theme):
        self.main_stylesheet = f"""
            background-color: {themes[theme]["background-color"]};
            color: {themes[theme]["color"]};
            border: {themes[theme]["border"]};
            border-radius: {themes["general"]["border-radius"]};
            padding: {themes["general"]["padding"]};
            """
        self.widget_stylesheet = f"""
            background-color: {themes[theme]["widget-background-color"]};
            """
        self.setStyleSheet(self.main_stylesheet)
        self.iterate_button.setStyleSheet(self.widget_stylesheet)
        self.most_recent_number_text.setStyleSheet(self.widget_stylesheet)
        self.most_recent_number.setStyleSheet(self.widget_stylesheet)
        self.most_recent_prime_text.setStyleSheet(self.widget_stylesheet)
        self.most_recent_prime.setStyleSheet(self.widget_stylesheet)
        self.check_button.setStyleSheet(self.widget_stylesheet)
        self.check_input.setStyleSheet(self.widget_stylesheet)
        self.check_output.setStyleSheet(self.widget_stylesheet)
        self.theme_toggle.setStyleSheet(self.widget_stylesheet)

        (
            self.theme_toggle.setText("Dark")
            if theme == "dark"
            else self.theme_toggle.setText("Light")
        )


def main():
    app = QApplication(sys.argv)
    main_window = PrimeNumberFinder()  # noqa: F841
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
