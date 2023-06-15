import sys
from struct import *
from PySide6.QtCore import QIODevice, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTextEdit
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

DEFAULT_WINDOW_SIZE = (650, 500)

ARDUINO_MICRO_VENDOR_ID = 9025;
ARDUINO_MICRO_PRODUCT_ID = 32823;

DEFAULT_KEYBOARD_LAYOUT = [194, 177, 212, 109, 121, 178, 218, 216, 217, 215]

class KeyboardInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.arduino = QSerialPort()
        self.currentLayout = DEFAULT_KEYBOARD_LAYOUT

        self.setWindowTitle("Keyboard Interface")
        # Increase Window Size
        self.resize(DEFAULT_WINDOW_SIZE[0], DEFAULT_WINDOW_SIZE[1])
        self.layout = QVBoxLayout()
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
                
        # Connected Device Name
        self.connected_device_name = QLabel(self)
        self.connected_device_name.setText("Connected Device: None")
        self.layout.addWidget(self.connected_device_name)

        # Manufacturer Number Input
        self.manufacturer_input = QLineEdit(self)
        self.layout.addWidget(self.manufacturer_input)

        # Download Layout Button
        self.downloadButton = QPushButton("Download", self)
        self.downloadButton.clicked.connect(self.download)
        self.layout.addWidget(self.downloadButton)

        # Upload Button
        self.uploadButton = QPushButton("Upload", self)
        self.uploadButton.clicked.connect(self.upload)
        self.layout.addWidget(self.uploadButton)

        # Console
        self.console = QTextEdit(self)
        self.console.setReadOnly(True)
        self.layout.addWidget(self.console)

        self.connect()

    def connect(self):
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
            self.connected_device_name.setText("Connected Device: " + portInfo.portName())
            break
        else:
            self.console.append("Could not find Arduino Micro")

    @Slot()
    def download(self):
        if not self.arduino.open(QSerialPort.ReadWrite):
            print("Could not connect")
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
    def upload(self):
        if not self.arduino.open(QSerialPort.ReadWrite):
            print("Could not connect")
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeyboardInterface()
    window.show()
    sys.exit(app.exec())