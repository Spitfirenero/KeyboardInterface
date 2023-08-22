import sys
import threading
from struct import *
from typing import Optional
from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QPushButton, QTextEdit
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

from MacroMapperSerial import MacroMapperSerial

DEFAULT_WINDOW_SIZE = (300, 550)

ARDUINO_MICRO_VENDOR_ID = 9025
# Arduino micro product id
# ARDUINO_MICRO_PRODUCT_ID = 32823

# Arduino mega product id
ARDUINO_MICRO_PRODUCT_ID = 66


class MacroMapper(QMainWindow):

    __currentLayout = []

    def __init__(self) -> None:
        super().__init__()

        # Setup External Packages
        self.serialConnection = MacroMapperSerial()
        self.serialConnection.scanSerialPorts(ARDUINO_MICRO_VENDOR_ID, ARDUINO_MICRO_PRODUCT_ID)
        self.serialConnection.connectToSerial()

        # Setup Window defaults
        self.setWindowTitle("Macro Mapper")
        self.resize(DEFAULT_WINDOW_SIZE[0], DEFAULT_WINDOW_SIZE[1])
        self.mainlayout = QVBoxLayout()
        self.centralWidget = QWidget(self)
        self.centralWidget.setLayout(self.mainlayout)
        self.setCentralWidget(self.centralWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MacroMapper()
    window.show()
    sys.exit(app.exec())

        