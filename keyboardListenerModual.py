from pynput import keyboard
from PySide6.QtCore import Signal, QObject

class KeyboardListener(QObject):

    keyPressed = Signal(int)

    def __init__(self):
        super().__init__()

        self.pyToArduino = {
            keyboard.Key.ctrl_l: 128,
            keyboard.Key.shift_l: 129,
            keyboard.Key.alt_l: 130,
            keyboard.Key.cmd_l: 131,
            keyboard.Key.ctrl_r: 132,
            keyboard.Key.shift_r: 133,
            keyboard.Key.alt_r: 134,
            keyboard.Key.cmd_r: 135,
            keyboard.Key.tab: 179,
            keyboard.Key.caps_lock: 193,
            keyboard.Key.backspace: 178,
            keyboard.Key.enter: 176,
            keyboard.Key.menu: 237,
            keyboard.Key.insert: 209,
            keyboard.Key.delete: 212,
            keyboard.Key.home: 210,
            keyboard.Key.end: 213,
            keyboard.Key.page_up: 211,
            keyboard.Key.page_down: 214,
            keyboard.Key.up: 218,
            keyboard.Key.down: 217,
            keyboard.Key.left: 216,
            keyboard.Key.right: 215,
            keyboard.Key.esc: 177,
            keyboard.Key.f1: 194,
            keyboard.Key.f2: 195,
            keyboard.Key.f3: 196,
            keyboard.Key.f4: 197,
            keyboard.Key.f5: 198,
            keyboard.Key.f6: 199,
            keyboard.Key.f7: 200,
            keyboard.Key.f8: 201,
            keyboard.Key.f9: 202,
            keyboard.Key.f10: 203,
            keyboard.Key.f11: 204,
            keyboard.Key.f12: 205,
            keyboard.Key.print_screen: 206,
            keyboard.Key.scroll_lock: 207,
            keyboard.Key.pause: 208
        }

        self.listener = keyboard.Listener(on_press=self.on_press)

    def start(self) -> None:
        self.listener.start()
        self.listener.join()

    def stop(self) -> None:
        self.listener.stop()

    def convertToArduino(self, key) -> int:
        try:
            return self.pyToArduino[key]
        except KeyError:
            return key.char.encode("latin_1")[0]

    def on_press(self, key) -> None:
        self.keyPressed.emit(self.convertToArduino(key))
        self.stop()

if __name__ == "__main__":
    listener = KeyboardListener()