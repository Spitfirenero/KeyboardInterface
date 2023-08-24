from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem, QStyleOptionGraphicsItem, QWidget, QGraphicsSceneMouseEvent
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QFont, QColor


class MacroMapperKeyGraphItem(QGraphicsItem):
    
    __text: QGraphicsTextItem = None
    __rect: QRectF = None


    def __init__(self, pos: tuple, size: tuple) -> None:
        super().__init__()

        self.__rect = QRectF(pos[0], pos[1], size[0], size[1])
        self.__text = QGraphicsTextItem()

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

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(event)

        self.__text.setDefaultTextColor(Qt.red)
        self.scene().clicked.emit(self)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        painter.setBrush(QColor('#404040'))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.__rect, 5, 5)

    def boundingRect(self) -> QRectF:
        return self.__rect