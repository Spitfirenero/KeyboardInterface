from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo


class MacroMapperSerial:

    __serialPortInfo: QSerialPortInfo
    __serialPort: QSerialPort

    __downloadCommand = b'D'
    __uploadCommand = b'U'

    def __init__(self):
        self.__serialPort = QSerialPort()

    def scanSerialPorts(self, vendorID: int, productID: int) -> None:
        availablePorts = QSerialPortInfo.availablePorts()
        for port in availablePorts:
            if port.vendorIdentifier() == vendorID and port.productIdentifier() == productID:
                self.__serialPortInfo = port
    
    def connectToSerial(self) -> bool:
        if self.__serialPortInfo == None:
            return False
        
        self.__serialPort.setPort(self.__serialPortInfo)
        self.__serialPort.setBaudRate(QSerialPort.Baud9600)
        self.__serialPort.setDataBits(QSerialPort.Data8)
        self.__serialPort.setParity(QSerialPort.NoParity)
        self.__serialPort.setStopBits(QSerialPort.OneStop)
        self.__serialPort.setFlowControl(QSerialPort.NoFlowControl)

        return True
    
    def download(self) -> list:
        if not self.__serialPort.open(QSerialPort.ReadWrite):
            return None
        
        self.__serialPort.setDataTerminalReady(True)
        self.__serialPort.write(self.__downloadCommand)

        self.__serialPort.waitForReadyRead()
        data = self.__serialPort.readAll().data().decode("latin_1")
        self.__serialPort.close()

        return [ord(c) for c in data]
    
    def upload(self, currentLayout: list) -> bool:
        if not self.__serialPort.open(QSerialPort.ReadWrite):
            return False
        
        command = self.__uploadCommand + bytes(currentLayout)

        self.__serialPort.setDataTerminalReady(True)
        self.__serialPort.write(command)

        self.__serialPort.waitForReadyRead()
        data = self.__serialPort.readAll().data().decode("latin_1")
        self.__serialPort.close()

        return data == "Ok"
