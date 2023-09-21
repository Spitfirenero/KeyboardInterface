from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtCore import Signal
from PySide6.QtGui import QPainter

from MacroMapperKeyGraphItem import MacroMapperKeyGraphItem
from MacroMapperSignalSlots import ConnectionManager, Signal, Slot


class MacroMapperKeyGraphScene(QGraphicsScene):
        __index: list
        __view: QGraphicsView
        
        __currentlySelected: MacroMapperKeyGraphItem = None
    
        def __init__(self):
            super().__init__()

            self.__index = []
            self.__view = QGraphicsView()
            self.__view.setScene(self)
            self.__view.setRenderHint(QPainter.Antialiasing)
    
        def addKeyboard(self, offset: int, size: int):
            verticalOffset = 0
            for i in range(0, 4):
                if i == 2:
                    verticalOffset = size / 2
                
                for j in range(0, 3):
                    if (i == 2 and j == 0) or (i == 2 and j == 2):
                        continue

                    key = MacroMapperKeyGraphItem((j * (size + offset), i * (size + offset) + verticalOffset), (size, size))
                    ConnectionManager().connect("clicked", self.keyPressed)
                    self.addItem(key)

        def keyPressed(self, key: MacroMapperKeyGraphItem):
             pass

        def getView(self) -> QGraphicsView:
            return self.__view