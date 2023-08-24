from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo


class MacroMapperSerial:

    __serialPort: QSerialPort = None

    __downloadCommand = b'D'
    __uploadCommand = b'U'

    def __init__(self) -> None:
        self.__serialPort = QSerialPort()
    
    def connectToSerial(self, vendorID: int, productID: int) -> bool:        
        availablePorts = QSerialPortInfo.availablePorts()
        for portInfo in availablePorts:
            if not portInfo.vendorIdentifier() == vendorID and not portInfo.productIdentifier() == productID:
                continue
            
            self.__serialPort.setPort(portInfo)
            self.__serialPort.setBaudRate(QSerialPort.Baud9600)
            self.__serialPort.setDataBits(QSerialPort.Data8)
            self.__serialPort.setParity(QSerialPort.NoParity)
            self.__serialPort.setStopBits(QSerialPort.OneStop)
            self.__serialPort.setFlowControl(QSerialPort.NoFlowControl)

            return True
        return False
    
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
