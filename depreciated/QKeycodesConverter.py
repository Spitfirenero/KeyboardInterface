from pynput import keyboard

class QKeycodesConverter:

    __conversionTable = [
        (keyboard.Key.ctrl_l, 128, "Left\nControl"),
        (keyboard.Key.shift_l, 129, "Left\nShift"),
        (keyboard.Key.alt_l, 130, "Left\nAlt"),
        (keyboard.Key.cmd_l, 131, "Left\nWindows"),
        (keyboard.Key.ctrl_r, 132, "Right\nControl"),
        (keyboard.Key.shift_r, 133, "Right\nShift"),
        (keyboard.Key.alt_r, 134, "Right\nAlt"),
        (keyboard.Key.cmd_r, 135, "Right\nWindows"),
        (keyboard.Key.tab, 179, "Tab"),
        (keyboard.Key.caps_lock, 193, "Caps\nLock"),
        (keyboard.Key.backspace, 178, "Backspace"),
        (keyboard.Key.enter, 176, "Enter"),
        (keyboard.Key.menu, 237, "Menu"),
        (keyboard.Key.insert, 209, "Insert"),
        (keyboard.Key.delete, 212, "Delete"),
        (keyboard.Key.home, 210, "Home"),
        (keyboard.Key.end, 213, "End"),
        (keyboard.Key.page_up, 211, "Page\nUp"),
        (keyboard.Key.page_down, 214, "Page\nDown"),
        (keyboard.Key.up, 218, "Up\nArrow"),
        (keyboard.Key.down, 217, "Down\nArrow"),
        (keyboard.Key.left, 216, "Left\nArrow"),
        (keyboard.Key.right, 215, "Right\nArrow"),
        (keyboard.Key.esc, 177, "Escape"),
        (keyboard.Key.f1, 194, "F1"),
        (keyboard.Key.f2, 195, "F2"),
        (keyboard.Key.f3, 196, "F3"),
        (keyboard.Key.f4, 197, "F4"),
        (keyboard.Key.f5, 198, "F5"),
        (keyboard.Key.f6, 199, "F6"),
        (keyboard.Key.f7, 200, "F7"),
        (keyboard.Key.f8, 201, "F8"),
        (keyboard.Key.f9, 202, "F9"),
        (keyboard.Key.f10, 203, "F10"),
        (keyboard.Key.f11, 204, "F11"),
        (keyboard.Key.f12, 205, "F12"),
        (keyboard.Key.print_screen, 206, "Print\nScreen"),
        (keyboard.Key.scroll_lock, 207, "Scroll\nLock"),
        (keyboard.Key.pause, 208, "Pause"),
        (keyboard.Key.space, 32, "Space")
    ]

    @classmethod
    def convertToPynput(cls, key: int) -> keyboard.Key:
        for conversion in cls.__conversionTable:
            if conversion[1] == key:
                return conversion[0]
        return key

    @classmethod
    def convertToLabel(cls, key: int) -> str:
        for conversion in cls.__conversionTable:
            if conversion[1] == key:
                return conversion[2]
        return chr(key)

    @classmethod
    def convertToArduino(cls, key: keyboard.Key) -> int:
        for conversion in cls.__conversionTable:
            if conversion[0] == key:
                return conversion[1]
        return key.char.encode("latin_1")[0]
