class SingletonMeta(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]

class ConnectionManager(metaclass=SingletonMeta):
    __listener = {}

    def connect(self, name, slot) -> None:
        if name not in self.__listener:
            self.__listener[name] = [slot]
            return
        
        self.__listener[name].append(slot)

    def emmit(self, name, *args, **kwargs) -> None:
        if name not in self.__listener:
            raise KeyError(f"No listener for: { name } found")
        
        for key in self.__listener:
            for slot in self.__listener[key]:
                slot(*args, **kwargs)

class Signal:
    __returnTypes: list[type]
    __name: str

    def __init__(self, name, *args) -> None:
        self.__returnTypes = []
        self.__name = name
        for arg in args:
            if not isinstance(arg, type):
                raise TypeError(f"Expected type, got { arg } instead")
            self.__returnTypes.append(arg)

    def emmit(self, *args, **kwargs) -> None:
        if len(args) != len(self.__returnTypes):
            raise TypeError(f"Expected { len(self.__returnTypes) } args, got { len(args) } instead")
        for i in range(len(args)):
            if not isinstance(args[i], self.__returnTypes[i]):
                raise TypeError(f"Expected { self.__returnTypes[i] } got { type(args[i]) } instead")
            
        ConnectionManager().emmit(self.__name, *args, **kwargs)


class Slot:
    __returnTypes: list[type]

    def __init__(self, *args) -> None:
        self.__returnTypes = []
        for arg in args:
            if not isinstance(arg, type):
                raise TypeError(f"Expected type, got { arg } instead")
            self.__returnTypes.append(arg)

    def __call__(self, func) -> object:
        def wrapper(*args, **kwargs):
            offset = 0
            if not isinstance(args[0], type):
                offset = 1
            if len(args) - offset != len(self.__returnTypes):
                raise TypeError(f"Expected { len(self.__returnTypes) - offset } args, got { len(args) } instead")
            for i in range(len(args) - offset):
                if not isinstance(args[i + offset], self.__returnTypes[i]):
                    raise TypeError(f"Expected { self.__returnTypes[i] } got { type(args[i + offset]) } instead")
            func(*args, **kwargs)
        return wrapper


sig = Signal("hello", str)

class Test:
    def __init__(self) -> None:
        ConnectionManager().connect("hello", self.a)
        # ConnectionManager().connect("hello", self.b)

    @Slot(str)
    def a(self, message: str) -> None:
        print(message)

    # @Slot(str)
    # def b(self, message: str) -> None:
    #     print(message)

Test()

def a(message: str) -> None:
    print(message)
ConnectionManager().connect("hello", a)
sig.emmit("Hello world!")
