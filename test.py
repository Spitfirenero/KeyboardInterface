import sys
import json
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QBrush
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem, QLineEdit, QGraphicsWidget, QGraphicsLinearLayout


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class QNode(QGraphicsItem):
    def __init__(self):
        super().__init__()

        with open('nodes.json') as f:
            self.layout = json.load(f)

    def boundingRect(self):
        return QRectF(0, 0, 100, 100)
    
    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(Qt.red))
        painter.drawRect(0, 0, 100, 100)

    def mousePressEvent(self, event) -> None:
        self.pos = event.pos()
        return super().mousePressEvent(event)


class QNodeEditor(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 400, 300)

    def addNode(self, position: Vector2, node: QNode):
        self.addItem(node)
        node.setPos(position.x, position.y)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Node Editor")
        self.nodeEditor = QNodeEditor()

        view = QGraphicsView(self.nodeEditor, self)
        view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(view)
        self.nodeEditor.addNode(Vector2(100, 100), QNode())

    def resizeEvent(self, event):
        if self.centralWidget() is not None:
            self.centralWidget().setGeometry(self.centralWidget().rect())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
