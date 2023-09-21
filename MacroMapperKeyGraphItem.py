from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem, QStyleOptionGraphicsItem, QWidget, QGraphicsSceneMouseEvent
from PySide6.QtCore import Qt, QRectF, QObject, Signal, Slot
from PySide6.QtGui import QPainter, QFont, QColor

from MacroMapperSignalSlots import ConnectionManager, Signal, Slot


class MacroMapperKeyGraphItem(QGraphicsItem):

    __text: QGraphicsTextItem
    __rect: QRectF

    __defaultColor: QColor = QColor('#404040')
    __selectedColor: QColor = QColor('#303030')

    __currentColor: QColor = __defaultColor

    def __init__(self, pos: tuple, size: tuple) -> None:
        self.__emmitSignal = Signal("clicked", MacroMapperKeyGraphItem)
        super().__init__()

        self.__rect = QRectF(pos[0], pos[1], size[0], size[1])
        self.__text = QGraphicsTextItem("", self)

        ConnectionManager().connect("clicked", self.deSelect)

        self.formatText()

    def formatText(self) -> None:
        self.__text.setPos(self.__rect.x() - 5, self.__rect.y())
        self.__text.setDefaultTextColor(Qt.white)
        self.__text.setFont(QFont("Arial", 9.5))

        self.__text.setTextWidth(self.__rect.width() + 10)

        textOption = self.__text.document().defaultTextOption()
        textOption.setAlignment(Qt.AlignCenter)
        self.__text.document().setDefaultTextOption(textOption)

    def setText(self, text: str) -> None:
        self.__text.setPlainText(text)
        self.update()

    def deSelect(self, item) -> None:
        if item != self:
            self.__currentColor = self.__defaultColor
            self.update()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() != Qt.LeftButton:
            return
        
        ConnectionManager().emmit("clicked", self)

        self.__currentColor = self.__selectedColor
        self.update()

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        painter.setBrush(self.__currentColor)
        painter.drawRoundedRect(self.__rect, 5, 5)

    def boundingRect(self) -> QRectF:
        return self.__rect