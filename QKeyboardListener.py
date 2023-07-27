from pynput import keyboard
from PySide6.QtCore import Signal, QObject

class QKeyboardListener(QObject):

    __isPaused = True

    keyPressed = Signal(keyboard.Key)

    def __init__(self):
        super().__init__()

        self.listener = keyboard.Listener(on_press=self.on_press)

    def run(self) -> None:
        self.listener.start()
        self.listener.join()

    def start(self) -> None:
        self.__isPaused = False

    def pause(self) -> None:
        self.__isPaused = True

    def stop(self) -> None:
        self.listener.stop()

    def on_press(self, key) -> None:
        if self.__isPaused:
            return
        
        self.keyPressed.emit(key)