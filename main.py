#!/usr/bin/env python3

from sys import argv
from ui import *


def main():
    # Initialise App
    app = QApplication(argv)
    app.setWindowIcon(QIcon("assets/img/qt-icon.png"))

    # Create Window
    w = Window()

    # Exit on Window close
    exit(app.exec_())


if __name__ == '__main__':
    main()
