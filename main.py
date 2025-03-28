import sys
import threading
from struct import *
from typing import Optional
from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QPushButton, QTextEdit

from MacroMapperSerial import MacroMapperSerial
from MacroMapperKeyGraphScene import MacroMapperKeyGraphScene
from MacroMapperKeyGraphItem import MacroMapperKeyGraphItem
from MacroMapperSignalSlots import ConnectionManager, Signal, Slot

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
        self.serialConnection.connectToSerial(ARDUINO_MICRO_VENDOR_ID, ARDUINO_MICRO_PRODUCT_ID)

        # Setup Window defaults
        self.setWindowTitle("Macro Mapper")
        self.resize(DEFAULT_WINDOW_SIZE[0], DEFAULT_WINDOW_SIZE[1])
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.centralWidget = QWidget(self)
        self.centralWidget.setLayout(self.mainlayout)
        self.setCentralWidget(self.centralWidget)

        # Setup the keyboard layout
        self.keyboardLayout = MacroMapperKeyGraphScene()
        self.keyboardLayout.addKeyboard(5, 50)

        ConnectionManager().connect("clicked", self.onKeyGraphPressed)
        self.mainlayout.addWidget(self.keyboardLayout.getView())

        self.horizontalLayout = QHBoxLayout()
        self.mainlayout.addLayout(self.horizontalLayout)

        self.textInput = QLineEdit()
        self.horizontalLayout.addWidget(self.textInput)

        self.listenButton = QPushButton("Listen")
        self.listenButton.clicked.connect(self.onListenButtonPressed)
        self.horizontalLayout.addWidget(self.listenButton)

    @Slot()
    def onListenButtonPressed(self) -> None:
        pass

    @Slot(MacroMapperKeyGraphItem)
    def onKeyGraphPressed(self, item: MacroMapperKeyGraphItem) -> None:
        item.setText("Windows\nKey")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MacroMapper()
    window.show()
    sys.exit(app.exec())
