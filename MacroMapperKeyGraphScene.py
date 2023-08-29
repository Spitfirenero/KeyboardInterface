from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtCore import Signal
from PySide6.QtGui import QPainter

from MacroMapperKeyGraphItem import MacroMapperKeyGraphItem


class MacroMapperKeyGraphScene(QGraphicsScene):
    
        clicked = Signal(MacroMapperKeyGraphItem)

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
                    self.__index.append(key)
                    self.addItem(key)

        def mousePressEvent(self, event):
            super().mousePressEvent(event)

            for item in self.items():
                if not item.boundingRect().contains(event.scenePos()):
                    continue

                if self.__currentlySelected is not None:
                    self.__currentlySelected.setSelected(False)

                self.clicked.emit(item)
                item.setSelected(True)
                self.__currentlySelected = item

                break

        def getView(self) -> QGraphicsView:
            return self.__view