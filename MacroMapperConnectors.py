class Emittable:
    def __init__(self):
        self._listeners = {}

    def connect(self, signal, slot):
        if signal not in self._listeners:
            self._listeners[signal] = []
        self._listeners[signal].append(slot)

    def disconnect(self, signal, slot):
        if signal in self._listeners and slot in self._listeners[signal]:
            self._listeners[signal].remove(slot)

    def emit(self, signal, *args, **kwargs):
        if signal in self._listeners:
            for slot in self._listeners[signal]:
                slot(*args, **kwargs)