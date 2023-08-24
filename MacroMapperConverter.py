from pynput.keyboard import Key

class MacroMapperConverter:

    __conversionTable = [
        (Key.ctrl_l, 128, "Left\nControl"),
        (Key.shift_l, 129, "Left\nShift"),
        (Key.alt_l, 130, "Left\nAlt"),
        (Key.cmd_l, 131, "Left\nWindows"),
        (Key.ctrl_r, 132, "Right\nControl"),
        (Key.shift_r, 133, "Right\nShift"),
        (Key.alt_r, 134, "Right\nAlt"),
        (Key.cmd_r, 135, "Right\nWindows"),
        (Key.tab, 179, "Tab"),
        (Key.caps_lock, 193, "Caps\nLock"),
        (Key.backspace, 178, "Backspace"),
        (Key.enter, 176, "Enter"),
        (Key.menu, 237, "Menu"),
        (Key.insert, 209, "Insert"),
        (Key.delete, 212, "Delete"),
        (Key.home, 210, "Home"),
        (Key.end, 213, "End"),
        (Key.page_up, 211, "Page\nUp"),
        (Key.page_down, 214, "Page\nDown"),
        (Key.up, 218, "Up\nArrow"),
        (Key.down, 217, "Down\nArrow"),
        (Key.left, 216, "Left\nArrow"),
        (Key.right, 215, "Right\nArrow"),
        (Key.esc, 177, "Escape"),
        (Key.f1, 194, "F1"),
        (Key.f2, 195, "F2"),
        (Key.f3, 196, "F3"),
        (Key.f4, 197, "F4"),
        (Key.f5, 198, "F5"),
        (Key.f6, 199, "F6"),
        (Key.f7, 200, "F7"),
        (Key.f8, 201, "F8"),
        (Key.f9, 202, "F9"),
        (Key.f10, 203, "F10"),
        (Key.f11, 204, "F11"),
        (Key.f12, 205, "F12"),
        (Key.print_screen, 206, "Print\nScreen"),
        (Key.scroll_lock, 207, "Scroll\nLock"),
        (Key.pause, 208, "Pause"),
        (Key.space, 32, "Space")
    ]

    @classmethod
    def convertToArduino(cls, key: Key) -> int:
        for conversion in cls.__conversionTable:
            if conversion[0] == key:
                return conversion[1]
        return ord(key.char)
    
    @classmethod
    def convertToLabel(cls, key: int) -> str:
        for conversion in cls.__conversionTable:
            if conversion[1] == key:
                return conversion[2]
        return chr(key)