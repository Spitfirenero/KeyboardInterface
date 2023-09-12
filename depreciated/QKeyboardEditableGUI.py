from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsTextItem
from PySide6.QtCore import Qt, Signal, QRectF
from PySide6.QtGui import QPainter, QFont, QColor


class RoundedSquareItem(QGraphicsItem):
    def __init__(self, pos, size, index):
        super().__init__()

        self.index = index
        self.rect = QRectF(pos[0], pos[1], size[0], size[1])

        self.text = QGraphicsTextItem('debug', self)
        self.text.setPos(pos[0] - 5, pos[1])
        self.text.setDefaultTextColor(Qt.white)
        self.text.setFont(QFont("Arial", 9.5))

        self.text.setTextWidth(self.rect.width() + 10)

        textOption = self.text.document().defaultTextOption()
        textOption.setAlignment(Qt.AlignCenter)
        self.text.document().setDefaultTextOption(textOption)

    def mousePressEvent(self, event):
        self.text.setDefaultTextColor(Qt.red)
        self.scene().clicked.emit(self)
        self.update()

    def mouseReleaseEvent(self, event) -> None:
        self.text.setDefaultTextColor(Qt.white)
        self.update()
 
    def paint(self, painter, a, s):
        painter.setBrush(QColor('#404040'))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect, 5, 5)

    def boundingRect(self) -> QRectF:
        return self.rect
    

class QKeyboardScene(QGraphicsScene):

    clicked = Signal(RoundedSquareItem)

    def __init__(self):
        super().__init__()


class QKeyboardEditableGUI(QGraphicsView):

    def __init__(self):
        super().__init__()
        
        self.scene = QKeyboardScene()
        self.index = []

        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)

    def addKeyboard(self, offset, size):
        verticalOffset = 0
        index = 0

        for i in range(0, 4):
            if i == 2:
                verticalOffset = size / 2

            for j in range(0, 3):
                if (i == 2 and j == 0) or (i == 2 and j == 2):
                    continue

                key = RoundedSquareItem((j * (size + offset), i * (size + offset) + verticalOffset), (size, size), index)
                self.index.append(key)
                self.scene.addItem(key)

                index += 1
