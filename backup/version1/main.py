import sys
import threading
from struct import *
from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QPushButton, QTextEdit
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

from QKeyboardListener import QKeyboardListener
from QKeycodesConverter import QKeycodesConverter
from QKeyboardEditableGUI import QKeyboardEditableGUI, RoundedSquareItem

from pynput import keyboard

DEFAULT_WINDOW_SIZE = (350, 550)

CONSOLE_MAX_SIZE = 120

MAX_CONNECTION_ATTEMPTS = 5

ARDUINO_MICRO_VENDOR_ID = 9025
ARDUINO_MICRO_PRODUCT_ID = 32823

DEFAULT_KEYBOARD_LAYOUT = [135, 177, 212, 109, 121, 178, 218, 216, 217, 215]

class QKeyboardInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.arduino = QSerialPort()
        self.currentLayout = DEFAULT_KEYBOARD_LAYOUT
        self.connectionAttempts = 0

        # Create the keyboard listener
        self.listener = QKeyboardListener()
        self.listener.keyPressed.connect(self.onKeyPressed)
        self.listenerThread = threading.Thread(target=self.listener.run, daemon=True)
        self.listenerThread.start()

        self.setWindowTitle("Keyboard Interface")
        # Increase Window Size
        self.resize(DEFAULT_WINDOW_SIZE[0], DEFAULT_WINDOW_SIZE[1])
        self.layout = QVBoxLayout()
        self.listenerLayout = QHBoxLayout()
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Keyboard Layout   
        self.keyboardLayout = QKeyboardEditableGUI()
        self.keyboardLayout.addKeyboard(5, 50)
        self.keyboardLayout.scene.clicked.connect(self.onGUIPressed)
        self.layout.addWidget(self.keyboardLayout)
                
        # Connected Device Name
        self.connected_device_name = QLabel(self)
        self.connected_device_name.setText("Connected Device: None")
        self.layout.addWidget(self.connected_device_name)

        # Download Layout Button
        self.downloadButton = QPushButton("Download", self)
        self.downloadButton.clicked.connect(self.download)
        self.layout.addWidget(self.downloadButton)

        # Upload Button
        self.uploadButton = QPushButton("Upload", self)
        self.uploadButton.clicked.connect(self.upload)
        self.layout.addWidget(self.uploadButton)

        # Keyboard Layout
        self.keyboardLayout = QLabel(self)
        self.keyboardLayout.setText("Keyboard Layout: " + str(self.currentLayout))
        self.layout.addWidget(self.keyboardLayout)

        self.layout.addLayout(self.listenerLayout)

        # Input Field
        self.listenerInput = QLineEdit()
        self.listenerLayout.addWidget(self.listenerInput)

        # Keyboard Listener
        self.keyboardListener = QPushButton("Start Keyboard Listener", self)
        self.keyboardListener.clicked.connect(self.startListener)
        self.listenerLayout.addWidget(self.keyboardListener)

        # Console
        self.console = QTextEdit(self)
        self.console.setReadOnly(True)
        self.console.setMaximumHeight(CONSOLE_MAX_SIZE)
        self.layout.addWidget(self.console)

        self.connect()
    
    def startListener(self) -> None:
        self.listener.start()

    def attemptConnect(self) -> None:
        while not self.arduino.open(QSerialPort.ReadWrite) and self.connectionAttempts <= MAX_CONNECTION_ATTEMPTS:
            self.connectionAttempts += 1
            self.connect()

        if self.connectionAttempts >= MAX_CONNECTION_ATTEMPTS:
            self.console.append("Max Connection Attempts Reached, Make Sure Arduino Micro is Plugged In")

        self.connectionAttempts = 0

    def connect(self) -> None:
        ports = QSerialPortInfo.availablePorts()

        for portInfo in ports:
            if portInfo.vendorIdentifier() != ARDUINO_MICRO_VENDOR_ID:
                continue
            if portInfo.productIdentifier() != ARDUINO_MICRO_PRODUCT_ID:
                continue
            
            self.arduino.setPort(portInfo)
            self.arduino.setBaudRate(QSerialPort.Baud9600)
            self.arduino.setDataBits(QSerialPort.Data8)
            self.arduino.setParity(QSerialPort.NoParity)
            self.arduino.setStopBits(QSerialPort.OneStop)
            self.arduino.setFlowControl(QSerialPort.NoFlowControl)
            self.connected_device_name.setText("Connected Device: " + portInfo.description())
            break
        else:
            self.console.append("Could not find Arduino Micro")

    @Slot(RoundedSquareItem)
    def onGUIPressed(self, key):
        key.text.setPlainText('Right\nWindows')
        key.update()

    @Slot(keyboard.Key)
    def onKeyPressed(self, key: keyboard.Key) -> None:
        arduinoKey = QKeycodesConverter.convertToArduino(key)
        labelKey = QKeycodesConverter.convertToLabel(arduinoKey)
        self.listenerInput.setText(labelKey)
        self.console.append("Key Pressed: " + labelKey)
        self.listener.pause()

    @Slot()
    def download(self) -> None:
        if not self.arduino.open(QSerialPort.ReadWrite):
            self.attemptConnect()
            return
        
        layout = []
        
        while len(layout) < 10:
            self.arduino.setDataTerminalReady(True)
            self.arduino.flush()
            self.arduino.write("D".encode())

            self.arduino.waitForReadyRead(1000)
            data = self.arduino.readAll().data().decode("latin_1")
            layout = [ord(c) for c in data]

        self.currentLayout = layout
        self.console.append("Downloaded Layout: " + str(self.currentLayout))
        self.arduino.close()

    @Slot()
    def upload(self) -> None:
        if not self.arduino.open(QSerialPort.ReadWrite):
            self.attemptConnect()
            return
        
        sendData = "U".encode() + bytes(self.currentLayout)
        self.arduino.setDataTerminalReady(True)
        self.arduino.write(sendData)

        self.arduino.waitForReadyRead(1000)
        data = self.arduino.readAll().data().decode("latin_1")

        self.arduino.close()

        if data == "Ok":
            self.console.append("Uploaded Layout: " + str(self.currentLayout))
        else:
            self.console.append("Upload Failed Due to Serial Error, Try Again")

    def closeEvent(self, event) -> None:
        super().closeEvent(event)
        self.listener.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QKeyboardInterface()
    window.show()
    sys.exit(app.exec())