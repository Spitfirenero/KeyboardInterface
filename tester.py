from PySide6.QtCore import Signal, QObject

class myTestObject(QObject):
    someSignal = Signal(str)

    def __init__(self):
        QObject.__init__(self)  # call to initialize properly
        self.someSignal.connect(self.testSignal)  # test connect
        self.someSignal.emit("Wowz")  # test

    def testSignal(self, arg):
        print("my signal test from init fire", arg)