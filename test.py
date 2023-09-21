class Signal:
    def __init__(self, returnType: type) -> None:
        self.__returnType = returnType
        self.__listeners = []

    def connect(self, slot):
        self.__listeners.append(slot)

    def disconnect(self, slot):
        self.__listeners.remove(slot)

    def emit(self, *args, **kwargs):
        for slot in self.__listeners:
            for arg in args:
                if not isinstance(arg, self.__returnType):
                    raise TypeError(f"Expected {self.__returnType} got {type(arg)}")
            slot(*args, **kwargs)


class Slot:
    def __init__(self, returnType: type) -> None:
        self.__returnType = returnType

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            for arg in args:
                if not isinstance(arg, self.__returnType):
                    raise TypeError(f"Expected {self.__returnType} got {type(arg)}")
            func(*args, **kwargs)
        return wrapper


# Example usage:
class MyWidget:
    def __init__(self):
        self.clickedSignal = Signal(str)

    def button_click(self):
        self.clickedSignal.emit("Hello World!", "fucker")

@Slot(str)
def print_message(message: str, ss: str):
    print(message + ss)

widget = MyWidget()
widget.clickedSignal.connect(print_message)

# Emulate a button click event
widget.button_click()  # Output: Hello, world!